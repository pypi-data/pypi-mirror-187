"""
Read and write objects to disk, read and write audio files, read SOFA files.

The functions :py:func:`read` and :py:func:`write` allow to save or load
several pyfar objects and other variables. So, e.g., workspaces in notebooks
can be stored. :py:class:`Signal <pyfar.signal.Signal>` objects can be
imported and exported as audio files using :py:func:`read_audio` and
:py:func:`write_audio`. :py:func:`read_sofa` provides functionality to read the
data stored in a SOFA file.
"""
import os.path
import pathlib

import warnings
import sofar as sf
import zipfile
import io
import numpy as np
import re

try:
    import soundfile
    soundfile_imported = True
except (ModuleNotFoundError, OSError):
    soundfile_imported = False
    soundfile_warning = (
        "python-soundfile could not be imported. Try to install it using `pip "
        "install soundfile`. If this not works search the documentation for "
        "help: https://python-soundfile.readthedocs.io")

from pyfar import Signal, FrequencyData, Coordinates, TimeData
from . import _codec as codec
import pyfar.classes.filter as fo


def read_sofa(filename, verify=True):
    """
    Import a SOFA file as pyfar object.

    Parameters
    ----------
    filename : string, Path
        Input SOFA file (cf. [#]_, [#]_).
    verify : bool, optional
        Verify if the data contained in the SOFA file agrees with the AES69
        standard (see references). If the verification fails, the SOFA file
        can be loaded by setting ``verify=False``. The default is ``True``

    Returns
    -------
    audio : pyfar audio object
        The audio object that is returned depends on the DataType of the SOFA
        object:

        - :py:class:`~pyfar.classes.audio.Signal`
            A Signal object is returned is the DataType is ``'FIR'``,
            ``'FIR-E'``, or ``'FIRE'``.
        - :py:class:`~pyfar.classes.audio.FrequencyData`
            A FrequencyData object is returned is the DataType is ``'TF'``,
            ``'TF-E'``, or ``'TFE'``.

        The `cshape` of the object is is ``(M, R)`` with `M` being the number
        of measurements and `R` being the number of receivers from the SOFA
        file.
    source_coordinates : Coordinates
        Coordinates object containing the data stored in
        `SOFA_object.SourcePosition`. The domain, convention and unit are
        automatically matched.
    receiver_coordinates : Coordinates
        Coordinates object containing the data stored in
        `SOFA_object.RecevierPosition`. The domain, convention and unit are
        automatically matched.

    Notes
    -----
    * This function uses the sofar package to read SOFA files [#]_.

    References
    ----------
    .. [#] https://www.sofaconventions.org
    .. [#] “AES69-2020: AES Standard for File Exchange-Spatial Acoustic Data
        File Format.”, 2020.
    .. [#] https://pyfar.org

    """

    sofa = sf.read_sofa(filename, verify)
    return convert_sofa(sofa)


def convert_sofa(sofa):
    """
    Convert SOFA object to pyfar object.

    Parameters
    ----------
    sofa : SOFA object
        A SOFA object read or generated by the sofar package ([#]_).

    Returns
    -------
    audio : pyfar audio object
        The audio object that is returned depends on the DataType of the SOFA
        object:

        - :py:class:`~pyfar.classes.audio.Signal`
            A Signal object is returned is the DataType is ``'FIR'``,
            ``'FIR-E'``, or ``'FIRE'``. In case of ``'FIR-E'``, the time data
            is returned with the `cshape` EMRN (samples are in the last
            dimension) and not MRNE as in the SOFA standard (emitters are in
            the last dimension).
        - :py:class:`~pyfar.classes.audio.FrequencyData`
            A FrequencyData object is returned is the DataType is ``'TF'``,
            ``'TF-E'``, or ``'TFE'``. In case of ``'TF-E'``, the frequency data
            is returned with the `cshape` EMRN (frequencies are in the last
            dimension) and not MRNE as in the SOFA standard (emitters are in
            the last dimension).

        The `cshape` of the object is is ``(M, R)`` with `M` being the number
        of measurements and `R` being the number of receivers from the SOFA
        file.
    source_coordinates : Coordinates
        Coordinates object containing the data stored in
        `SOFA_object.SourcePosition`. The domain, convention and unit are
        automatically matched.
    receiver_coordinates : Coordinates
        Coordinates object containing the data stored in
        `SOFA_object.RecevierPosition`. The domain, convention and unit are
        automatically matched.

    References
    ----------
    .. [#] https://pyfar.org
    """

    # check input
    if not isinstance(sofa, sf.Sofa):
        raise TypeError((
            "Input must be a sofar.Sofa object "
            f"but is of type {str(type(sofa))}"))

    # Check for DataType
    if sofa.GLOBAL_DataType in ['FIR', 'FIR-E', 'FIRE']:
        # order axis according to pyfar convention
        # (samples go in last dimension)
        if sofa.GLOBAL_DataType == 'FIR-E':
            time = np.moveaxis(sofa.Data_IR, -1, 0)
        else:
            time = sofa.Data_IR

        # make a Signal
        signal = Signal(time, sofa.Data_SamplingRate)

    elif sofa.GLOBAL_DataType in ['TF', 'TF-E', 'TFE']:
        # order axis according to pyfar convention
        # frequencies go in last dimension)
        if sofa.GLOBAL_DataType == 'TF-E':
            freq = np.moveaxis(sofa.Data_Real, -1, 0) + \
                1j * np.moveaxis(sofa.Data_Imag, -1, 0)
        else:
            freq = sofa.Data_Real + 1j * sofa.Data_Imag

        # make FrequencyData
        signal = FrequencyData(freq, sofa.N)
    else:
        raise ValueError(
            f"DataType {sofa.GLOBAL_DataType} is not supported.")

    # Source
    s_values = sofa.SourcePosition
    s_domain, s_convention, s_unit = _sofa_pos(sofa.SourcePosition_Type)
    source_coordinates = Coordinates(
        s_values[:, 0],
        s_values[:, 1],
        s_values[:, 2],
        domain=s_domain,
        convention=s_convention,
        unit=s_unit)
    # Receiver
    r_values = sofa.ReceiverPosition
    r_domain, r_convention, r_unit = _sofa_pos(sofa.ReceiverPosition_Type)
    receiver_coordinates = Coordinates(
        r_values[:, 0],
        r_values[:, 1],
        r_values[:, 2],
        domain=r_domain,
        convention=r_convention,
        unit=r_unit)

    return signal, source_coordinates, receiver_coordinates


def _sofa_pos(pos_type):
    if pos_type == 'spherical':
        domain = 'sph'
        convention = 'top_elev'
        unit = 'deg'
    elif pos_type == 'cartesian':
        domain = 'cart'
        convention = 'right'
        unit = 'met'
    else:
        raise ValueError("Position:Type {pos_type} is not supported.")
    return domain, convention, unit


def read(filename):
    """
    Read any compatible pyfar object or numpy array (.far file) from disk.

    Parameters
    ----------
    filename : string, Path
        Input file. If no extension is provided, .far-suffix is added.

    Returns
    -------
    collection: dict
        Contains pyfar objects like
        ``{ 'name1': 'obj1', 'name2': 'obj2' ... }``.

    Examples
    --------
    Read signal and orientations objects stored in a .far file.

    >>> collection = pyfar.read('my_objs.far')
    >>> my_signal = collection['my_signal']
    >>> my_orientations = collection['my_orientations']
    """
    # Check for .far file extension
    filename = pathlib.Path(filename).with_suffix('.far')

    collection = {}
    with open(filename, 'rb') as f:
        zip_buffer = io.BytesIO()
        zip_buffer.write(f.read())
        with zipfile.ZipFile(zip_buffer) as zip_file:
            zip_paths = zip_file.namelist()
            obj_names_hints = [
                path.split('/')[:2] for path in zip_paths if '/$' in path]
            for name, hint in obj_names_hints:
                if codec._is_pyfar_type(hint[1:]):
                    obj = codec._decode_object_json_aided(name, hint, zip_file)
                elif hint == '$ndarray':
                    obj = codec._decode_ndarray(f'{name}/{hint}', zip_file)
                else:
                    raise TypeError(
                        '.far-file contains unknown types.'
                        'This might occur when writing and reading files with'
                        'different versions of Pyfar.')
                collection[name] = obj

        if 'builtin_wrapper' in collection:
            for key, value in collection['builtin_wrapper'].items():
                collection[key] = value
            collection.pop('builtin_wrapper')

    return collection


def write(filename, compress=False, **objs):
    """
    Write any compatible pyfar object or numpy array and often used builtin
    types as .far file to disk.

    Parameters
    ----------
    filename : string
        Full path or filename. If now extension is provided, .far-suffix
        will be add to filename.
    compress : bool
        Default is ``False`` (uncompressed).
        Compressed files take less disk space but need more time for writing
        and reading.
    **objs:
        Objects to be saved as key-value arguments, e.g.,
        ``name1=object1, name2=object2``.

    Examples
    --------

    Save Signal object, Orientations objects and numpy array to disk.

    >>> s = pyfar.Signal([1, 2, 3], 44100)
    >>> o = pyfar.Orientations.from_view_up([1, 0, 0], [0, 1, 0])
    >>> a = np.array([1,2,3])
    >>> pyfar.io.write('my_objs.far', signal=s, orientations=o, array=a)

    Notes
    -----
    * Supported builtin types are:
      bool, bytes, complex, float, frozenset, int, list, set, str and tuple
    """
    # Check for .far file extension
    filename = pathlib.Path(filename).with_suffix('.far')
    compression = zipfile.ZIP_STORED if compress else zipfile.ZIP_DEFLATED
    zip_buffer = io.BytesIO()
    builtin_wrapper = codec.BuiltinsWrapper()
    with zipfile.ZipFile(zip_buffer, "a", compression) as zip_file:
        for name, obj in objs.items():
            if codec._is_pyfar_type(obj):
                codec._encode_object_json_aided(obj, name, zip_file)
            elif codec._is_numpy_type(obj):
                codec._encode({f'${type(obj).__name__}': obj}, name, zip_file)
            elif type(obj) in codec._supported_builtin_types():
                builtin_wrapper[name] = obj
            else:
                error = (
                    f'Objects of type {type(obj)} cannot be written to disk.')
                if isinstance(obj, fo.Filter):
                    error = f'{error}. Consider casting to {fo.Filter}'
                raise TypeError(error)

        if len(builtin_wrapper) > 0:
            codec._encode_object_json_aided(
                builtin_wrapper, 'builtin_wrapper', zip_file)

    with open(filename, 'wb') as f:
        f.write(zip_buffer.getvalue())


def read_audio(filename, dtype='float64', **kwargs):
    """
    Import an audio file as :py:class:`~pyfar.classes.audio.Signal` object.

    Reads 'wav', 'aiff', 'ogg', 'flac', and 'mp3' files among others. For a
    complete list see :py:func:`audio_formats`.

    Parameters
    ----------
    filename : string, Path
        Input file.
    dtype : {'float64', 'float32', 'int32', 'int16'}, optional
        Data type to which the data in the wav file is casted, by default
        ``'float64'``. Floating point audio data is typically in the range from
        ``-1.0`` to ``1.0``.  Note that ``'int16'`` and ``'int32'`` should only
        be used if the data was written in the same format. Integer data is in
        the range from ``-2**15`` to ``2**15-1`` for ``'int16'`` and from
        ``-2**31`` to ``2**31-1`` for ``'int32'``. In any case, the data is
        converted to float.
    **kwargs
        Other keyword arguments to be passed to :py:func:`soundfile.read`. This
        is needed, e.g, to read RAW audio files.

    Returns
    -------
    signal : Signal
        :py:class:`~pyfar.classes.audio.Signal` object containing the audio
        data.

    Notes
    -----
    * This function is based on :py:func:`soundfile.read`.
    * Reading int values from a float file will *not* scale the data to
      [-1.0, 1.0). If the file contains ``np.array([42.6], dtype='float32')``,
      you will read ``np.array([43], dtype='int32')`` for ``dtype='int32'``.
    """
    if not soundfile_imported:
        warnings.warn(soundfile_warning)
        return

    data, sampling_rate = soundfile.read(
        file=filename, dtype=dtype, always_2d=True, **kwargs)

    return Signal(data.T, sampling_rate, domain='time')


def write_audio(signal, filename, subtype=None, overwrite=True, **kwargs):
    """
    Write a :py:class:`~pyfar.classes.audio.Signal` object as an audio file to
    disk.

    Writes 'wav', 'aiff', 'ogg', 'flac' and 'mp3' files among others. For a
    complete list see :py:func:`audio_formats`.

    Parameters
    ----------
    signal : Signal
        Object to be written.
    filename : string, Path
        Output file. The format is determined from the file extension.
        See :py:func:`audio_formats` for all possible formats.
    subtype : str, optional
        The subtype of the sound file, the default value depends on the
        selected `format` (see :py:func:`default_audio_subtype`).
        See :py:func:`audio_subtypes` for all possible subtypes for
        a given ``format``.
    overwrite : bool
        Select wether to overwrite the audio file, if it already exists.
        The default is ``True``.
    **kwargs
        Other keyword arguments to be passed to :py:func:`soundfile.write`.

    Notes
    -----
    * Signals are flattened before writing to disk (e.g. a signal with
      ``cshape = (3, 2)`` will be written to disk as a six channel audio file).
    * This function is based on :py:func:`soundfile.write`.
    * Except for the subtypes ``'FLOAT'``, ``'DOUBLE'`` and ``'VORBIS'`` ´
      amplitudes larger than +/- 1 are clipped.

    """
    if not soundfile_imported:
        warnings.warn(soundfile_warning)
        return

    sampling_rate = signal.sampling_rate
    data = signal.time

    # Reshape to 2D
    data = data.reshape(-1, data.shape[-1])
    if len(signal.cshape) != 1:
        warnings.warn(f"Signal flattened to {data.shape[0]} channels.")

    # Check if file exists and for overwrite
    if overwrite is False and os.path.isfile(filename):
        raise FileExistsError(
            "File already exists,"
            "use overwrite option to disable error.")
    else:
        # Only the subtypes FLOAT, DOUBLE, VORBIS are not clipped,
        # see _clipped_audio_subtypes()
        format = pathlib.Path(filename).suffix[1:]
        if subtype is None:
            subtype = default_audio_subtype(format)
        if (np.any(data > 1.) and
                subtype.upper() not in ['FLOAT', 'DOUBLE', 'VORBIS']):
            warnings.warn(
                f'{format}-files of subtype {subtype} are clipped to +/- 1.')
        soundfile.write(
            file=filename, data=data.T, samplerate=sampling_rate,
            subtype=subtype, **kwargs)


def audio_formats():
    """Return a dictionary of available audio formats.

    Notes
    -----
    This function is a wrapper of :py:func:`soundfile.available_formats()`.

    Examples
    --------
    >>> import pyfar as pf
    >>> pf.io.audio_formats()
    {'FLAC': 'FLAC (FLAC Lossless Audio Codec)',
     'OGG': 'OGG (OGG Container format)',
     'WAV': 'WAV (Microsoft)',
     'AIFF': 'AIFF (Apple/SGI)',
     ...
     'WAVEX': 'WAVEX (Microsoft)',
     'RAW': 'RAW (header-less)',
     'MAT5': 'MAT5 (GNU Octave 2.1 / Matlab 5.0)'}

    """
    if not soundfile_imported:
        warnings.warn(soundfile_warning)
        return

    return soundfile.available_formats()


def audio_subtypes(format=None):
    """Return a dictionary of available audio subtypes.

    Parameters
    ----------
    format : str
        If given, only compatible subtypes are returned.

    Notes
    -----
    This function is a wrapper of :py:func:`soundfile.available_subtypes()`.

    Examples
    --------
    >>> import pyfar as pf
    >>> pf.io.audio_subtypes('FLAC')
    {'PCM_24': 'Signed 24 bit PCM',
     'PCM_16': 'Signed 16 bit PCM',
     'PCM_S8': 'Signed 8 bit PCM'}

    """
    if not soundfile_imported:
        warnings.warn(soundfile_warning)
        return

    return soundfile.available_subtypes(format=format)


def default_audio_subtype(format):
    """Return the default subtype for a given format.

    Notes
    -----
    This function is a wrapper of :py:func:`soundfile.default_audio_subtype()`.

    Examples
    --------
    >>> import pyfar as pf
    >>> pf.io.default_audio_subtype('WAV')
    'PCM_16'
    >>> pf.io.default_audio_subtype('MAT5')
    'DOUBLE'

    """
    if not soundfile_imported:
        warnings.warn(soundfile_warning)
        return

    return soundfile.default_subtype(format)


def read_comsol(filename, expressions=None, parameters=None):
    """Read data exported from COMSOL Multiphysics.

    .. note::
        The data is created by defining at least one `Expression` within a
        `Data` node in Comsol's `Results/Export` section. The `data format`
        needs to be `Spreadsheet`. This function supports several `Expressions`
        as well as results for `Parametric Sweeps`.
        For more information see
        :py:func:`~pyfar.io.read_comsol_header`.

    Parameters
    ----------
    filename : str, Path
        Input file. Excepted input files are .txt, .dat and .csv. .csv-
        files are strongly recommended, since .txt and .dat-files vary in their
        format definitions.
    expressions : list of strings, optional
        This parameter defines which parts of the COMSOL data is
        returned as a pyfar FrequencyData or TimeData object. By default, all
        expressions are returned. COMSOL terminology is used, e.g.,
        ``expressions=['pabe.p_t']``.
        Further information and a list of all expressions can be obtained with
        :py:func:`~pyfar.io.read_comsol_header`.
    parameters : dict, optional
        COMSOL supports `Parametric Sweeps` to vary certain parameters in a
        sequence of simulations. The `parameters` dict contains the parameters
        and the their values that are to be returned.
        For example, in a study with a varying angle, the dict could be
        ``parameters={'theta': [0.0, 0.7854], 'phi': [0., 1.5708]}``.
        A list of all parameters included in a file can be obtained with
        :py:func:`~pyfar.io.read_comsol_header`. The default is ``None``, which
        means all parameters are included.

    Returns
    -------
    data : FrequencyData, TimeData
        Returns a TimeData or FrequencyData object depending the domain of the
        input data. The output has the `cshape` (#points, #expressions,
        #parameter1, #parameter2, ...). In case of missing parameter value
        combinations in the input, the missing data is filled with nans.
        If the input does not include parameters, the `cshape` is just
        (#points, #expressions).
    coordinates : Coordinates
        Evaluation points extracted from the input file as Coordinates object.
        The coordinate system is always cartesian. If the input dimension is
        lower than three, missing dimensions are filled with zeros.
        If the input file does not include evaluation points (e.g., in case of
        non-local datasets such as averages or integrals) no `coordinates` are
        returned.

    Examples
    --------
    Assume a `Pressure Acoustics BEM Simulation` (named "pabe" in COMSOL) for
    two frequencies including a `Parametric Sweep` with `All Combinations` of
    certain incident angles theta and phi for the incident sound wave.
    The sound pressure ("p_t") is exported to a file `comsol_sample.csv`.

    Obtain information on the input file with
    :py:func:`~pyfar.io.read_comsol_header`.

    >>> expressions, units, parameters, domain, domain_data = \\
    >>>     pf.io.read_comsol_header('comsol_sample.csv')
    >>> expressions
    ['pabe.p_t']
    >>> units
    ['Pa']
    >>> parameters
    {'theta': [0.0, 0.7854, 1.5708, 2.3562, 3.1416],
     'phi': [0.0, 1.5708, 3.1416, 4.7124]}
    >>> domain
    'freq'
    >>> domain_data
    [100.0, 500.0]

    Read the data including all parameter combinations.

    >>> data, coordinates = pf.io.read_comsol('comsol_sample.csv')
    >>> data
    FrequencyData:
    (8, 1, 5, 4) channels with 2 frequencies
    >>> coordinates
    1D Coordinates object with 8 points of cshape (8,)
    domain: cart, convention: right, unit: met
    coordinates: x in meters, y in meters, z in meters
    Does not contain sampling weights

    Read the data with a subset of the parameters.

    >>> parameter_subset = {
            'theta': [1.5708, 2.3562, 3.1416],
            'phi': [0.0, 1.5708, 3.1416, 4.7124]}
    >>> data, coordinates = pf.io.read_comsol(
    >>>     'comsol_sample.csv', parameters=parameter_subset)
    >>> data
    FrequencyData:
    (8, 1, 3, 4) channels with 2 frequencies
    """

    # check Datatype
    suffix = pathlib.Path(filename).suffix
    if suffix not in ['.txt', '.dat', '.csv']:
        raise SyntaxError((
            "Input path must be a .txt, .csv or .dat file"
            f"but is of type {str(suffix)}"))

    # get header
    all_expressions, units, all_parameters, domain, domain_data \
        = read_comsol_header(filename)
    if 'dB' in units:
        warnings.warn(
            r'The data contains values in dB. Consider to use de-logarithmize '
            r'data, such as sound pressure, if possible. otherwise any '
            r'further processing of the data might lead to erroneous results.')
    header, is_complex, delimiter = _read_comsol_get_headerline(filename)

    # set default variables
    if expressions is None:
        expressions = all_expressions.copy()
    if parameters is None:
        parameters = all_parameters.copy()

    # get meta data
    metadata = _read_comsol_metadata(filename)
    n_dimension = metadata['Dimension']
    n_nodes = metadata['Nodes']
    n_entries = metadata['Expressions']

    # read data
    dtype = complex if is_complex else float
    domain_str = domain if domain == 'freq' else 't'
    raw_data = np.loadtxt(
        filename, dtype=dtype, comments='%', delimiter=delimiter,
        converters=lambda s: s.replace('i', 'j'), encoding=None)
    # force raw_data to 2D
    raw_data = np.reshape(raw_data, (n_nodes, n_entries+n_dimension))

    # Define pattern for regular expressions, see test files for examples
    exp_pattern = r'([\w\/\^\*\(\)_.]+) \('
    domain_pattern = domain_str + r'=([0-9.]+)'
    value_pattern = r'=([0-9.]+)'

    # read parameter and header data
    expressions_header = np.array(re.findall(exp_pattern, header))
    domain_header = np.array(
        [float(x) for x in re.findall(domain_pattern, header)])
    parameter_header = dict()
    for key in parameters:
        parameter_header[key] = np.array(
            [float(x) for x in re.findall(key+value_pattern, header)])

    # final data shape
    final_shape = [n_nodes, len(expressions)]
    for key in parameters:
        final_shape.append(len(parameters[key]))
    final_shape.append(len(domain_data))

    # temporary shape
    n_combinations = np.prod(final_shape[2:-1]) if parameters else 1
    temp_shape = [n_nodes, len(expressions), n_combinations, len(domain_data)]

    # create pairs of parameter values
    pairs = np.meshgrid(*[x for x in parameters.values()])
    parameter_pairs = dict()
    for idx, key in enumerate(parameters):
        parameter_pairs[key] = pairs[idx].T.flatten()

    # loop over expressions, domain, parameters
    # extract the data by comparing with header
    # first fill the array with temporary shape, then reshape
    data_in = raw_data[:, -n_entries:]
    data_out = np.full(temp_shape, np.nan, dtype=dtype)
    for expression_idx, expression_key in enumerate(expressions):
        expression_mask = expressions_header == expression_key
        for parameter_idx in range(temp_shape[2]):
            parameter_mask = np.full_like(expression_mask, True)
            for key in parameters:
                parameter_mask &= parameter_header[key] \
                    == parameter_pairs[key][parameter_idx]
            for domain_idx, domain_value in enumerate(domain_data):
                domain_mask = domain_header == domain_value
                mask = parameter_mask & domain_mask & expression_mask
                if any(mask):
                    data_out[:, expression_idx, parameter_idx, domain_idx] \
                        = data_in[:, mask].flatten()
                else:
                    if parameters == all_parameters:
                        warnings.warn(
                            r'Specific combinations is set in the Parametric '
                            r'Sweep in Comsol. Missing data is filled with '
                            r'nans.')

    # reshape data to final shape
    data_out = np.reshape(data_out, final_shape)

    # create object
    comment = ', '.join(' '.join(x) for x in zip(all_expressions, units))
    if domain == 'freq':
        data = FrequencyData(data_out, domain_data, comment=comment)
    else:
        data = TimeData(data_out, domain_data, comment=comment)

    # create coordinates
    if n_dimension > 0:
        coords_data = np.real(raw_data[:, 0:n_dimension])
        x = coords_data[:, 0]
        y = coords_data[:, 1] if n_dimension > 1 else np.zeros_like(x)
        z = coords_data[:, 2] if n_dimension > 2 else np.zeros_like(x)
        coordinates = Coordinates(x, y, z)
        return data, coordinates
    else:
        return data


def read_comsol_header(filename):
    """Read header information on exported data from COMSOL Multiphysics.

    .. note::
        The data is created by defining at least one `Expression` within a
        `Data` node in Comsol's `Results/Export` section. The `data format`
        needs to be `Spreadsheet`. This function supports several `Expressions`
        as well as results for `Parametric Sweeps`.
        For more information see below.

    Parameters
    ----------
    filename : str, Path
        Input file. Excepted input files are .txt, .dat and .csv. .csv-
        files are strongly recommended, since .txt and .dat-files vary in their
        format definitions.

    Returns
    -------
    expressions : list of strings
        When exporting data in COMSOL, certain `Expressions` need to be
        specified that define the physical quantities to be exported. This
        function returns the expressions as a list, e.g.,
        ``expressions=['pabe.p_t']``.
    units : list of strings
        List of the units corresponding to `expressions`, e.g.,
        ``units=['Pa']``.
    parameters : dict
        COMSOL supports `Parametric Sweeps` to vary certain parameters in a
        sequence of simulations. This function returns the parameters
        and the parameter values as a dict. For example, in a study with a
        varying angle, the dict could be ``parameters={'theta': [0.0, 0.7854],
        'phi': [0., 1.5708]}``. If the input does not include parameters, an
        emtpy dict is returnd. Note that the dict is same for
        `All Combinations` and `Specific Combinations` of parameters as a
        distinction is not possible due to the data format.
    domain : string
        Domain of the input data. Only time domain (``'time'``) or
        frequency domain (``'freq'``) simulations are supported.
    domain_data : list
        List containing the sampling times or frequency bins depending
        on the domain of the data in the input file.

    Examples
    --------
    Assume a `Pressure Acoustics BEM Simulation` (named "pabe" in COMSOL) for
    two frequencies 100 Hz and 500 Hz including a `Parametric Sweep` of certain
    incident angles theta and phi for the incident sound wave. The sound
    pressure ("p_t") is exported to a file `comsol_sample.csv`.

    Obtain information on the input file.

    >>> expressions, units, parameters, domain, domain_data = \\
    >>>     pf.io.read_comsol_header('comsol_sample.csv')
    >>> expressions
    ['pabe.p_t']
    >>> units
    ['Pa']
    >>> parameters
    {'theta': [0.0, 0.7854, 1.5708, 2.3562, 3.1416],
     'phi': [0.0, 1.5708, 3.1416, 4.7124]}
    >>> domain
    'freq'
    >>> domain_data
    [100.0, 500.0]
    """
    # Check Datatype
    suffix = pathlib.Path(filename).suffix
    if not suffix.endswith(('.txt', '.dat', '.csv')):
        raise SyntaxError((
            "Input path must be a .txt, .csv or .dat file"
            f"but is of type {str(suffix)}"))

    # read header
    header, _, _ = _read_comsol_get_headerline(filename)

    # Define pattern for regular expressions, see test files for examples
    exp_unit_pattern = r'([\w\(\)\/\^\*. ]+) @'
    exp_pattern = r'([\w\/\^\*\(\)_.]+) \('
    unit_pattern = r'\(([\w\/\^\* .]+)\) @'
    domain_pattern = r'@ ([a-zA-Z]+)='
    value_pattern = r'=([0-9.]+)'
    param_pattern = r'([\w\/\^_.]+)='
    param_unit_pattern = r'=[0-9.]+([a-zA-Z]+)'

    # read expressions
    expressions_with_unit = re.findall(exp_unit_pattern, header)
    expressions_all = re.findall(exp_pattern, ';'.join(expressions_with_unit))
    expressions = _unique_strings(expressions_all)
    # read corresponding units
    exp_idxs = [expressions_all.index(e) for e in expressions]
    units_all = re.findall(unit_pattern, header)
    units = [units_all[i] for i in exp_idxs]

    # read domain data
    domain_str = re.findall(domain_pattern, header)[0]
    if domain_str == 't':
        domain = 'time'
    elif domain_str == 'freq':
        domain = domain_str
    else:
        raise ValueError(
            f"Domain can be 'time' or 'freq', but is {domain_str}.")
    domain_data = _unique_strings(
            re.findall(domain_str + value_pattern, header))
    domain_data = [float(d) for d in domain_data]

    # create parameters dict
    parameter_names = _unique_strings(re.findall(param_pattern, header))
    parameter_names.remove(domain_str)
    parameters = dict()
    for para_name in parameter_names:
        unit = _unique_strings(
            re.findall(para_name + param_unit_pattern, header))
        values = _unique_strings(
            re.findall(para_name + value_pattern, header))
        values = [float(v) for v in values]
        parameters[para_name] = [x+unit for x in values] if unit else values

    return expressions, units, parameters, domain, domain_data


def _read_comsol_metadata(filename):
    suffix = pathlib.Path(filename).suffix
    metadata = dict()
    # loop over meta data lines (starting with %)
    number_names = ['Dimension', 'Nodes', 'Expressions']
    with open(filename) as f:
        for line in f.readlines():
            if line[0] != '%':
                break
            elif any(n in line for n in number_names):
                # character replacements, splits
                line = line.lstrip('% ')
                if suffix == '.csv':
                    line = line.replace('"', '').split(',')
                elif suffix in ['.dat', '.txt']:
                    line = line.replace(',', ';').replace(':', ',').split(',')
                metadata[line[0]] = int(line[-1])
    return metadata


def _unique_strings(expression_list):
    unique = []
    for e in expression_list:
        if e not in unique:
            unique.append(e)
    return unique


def _read_comsol_get_headerline(filename):
    header = []
    with open(filename) as f:
        last_line = []
        for line in f.readlines():
            if not line.startswith('%'):
                header = last_line
                break
            last_line = line

    is_complex = 'i' in line
    delimiter = ',' if ',' in line else None
    return header, is_complex, delimiter
