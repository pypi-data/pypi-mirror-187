

if __name__ == "popyrous.timeseries.datasets":
    from .sliding_window import sliding_window
else:
    from sliding_window import sliding_window
    
    
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler


class TabularDataset:
    DTYPE = np.float32
    POWERS_OF_TWO = True
    def __init__(self, 
        input_vec, in_seq_length:int, in_features:int, in_squeezed:bool,
        output_vec=None, out_seq_length:int=1, out_features:int=0, out_squeezed:bool=True,
        data_downsampling_rate:int=1, sequence_downsampling_rate:int=1, 
        input_scaling:bool=True, output_scaling:bool=True,
        input_forward_facing:bool=True, output_forward_facing:bool=True,
        input_include_current_timestep:bool=True, output_include_current_timestep:bool=True,
        input_towards_future:bool=False, output_towards_future:bool=True,
        stacked=True, extern_input_scaler=None, extern_output_scaler=None, scaling:str='standard', verbose=True):
        """Generate 3D-tabulated dataset using sliding window from multi-variate timeseries data to be used later in 
        timeseries classification,. regression, deep learning, PyTorch dataloaders, etc.

        ### Parameters:

        :param `input_vec` (numpy array):               [Nx1] vector of timeseries inputs.
        :param `in_seq_length` (int):                   Input sequence length (sliding time window length)
        :param `in_features` (int)                      Number of features of input
        :param `in_squeezed` (bool):                    Squeezed inputs (batch, seqlen*features) as in ANNs 
                                                        or unsqueezed (batch, seqlen, features) as in LSTM
        :param `output_vec` (numpy array):              [Nx1] vector of timeseries outputs (targets). 
                                                        Default is the same as inputs (for autoregression).
        :param `out_seq_length` (int):                  Output (target) sequence length (sliding time window length).
                                                        Default is 1 (estimation rather than forecasting)
        :param `out_features` (int):                    Number of features of the output target. Default is 0.
        :param `out_squeezed` (bool):                   Squeezed inputs (batch, seqlen*features) as in Dense outputs
                                                        or unsqueezed (batch, seqlen, features) as in RNN outputs
        :param `data_downsampling_rate` (int):          Downsampling rate, if the data has too high sampling rate.
                                                        This integer must be greater than or equal to 1.
        :param `sequence_downsampling_rate` (int):      Downsampling rate, if the sequence has too high sampling rate.
        :param `input_scaling` (bool):                  Whether standard scaling should be applied to inputs. 
                                                        Default is True.
        :param `output_scaling` (bool):                 Whether standard scaling should be applied to output targets. 
                                                        Default is True.
        :param `input_forward_facing` (bool):           Whether the input sequences should be forward facing 
                                                        (timestep t-K towards K) or not (backward facing). 
                                                        Default is True.
        :param `output_forward_facing` (bool):          Whether the output target sequences should be forward facing. 
                                                        Default is True.
        :param `input_include_current_timestep`(bool):  Whether the input sequences include the current time step. 
                                                        Default is True.
        :param `output_include_current_timestep`(bool): Whether the input sequences include the current time step.
                                                        Default is False, for autoregression.
        :param `input_towards_future` (bool):           Whether the input sequences come from future data at 
                                                        every time step rather than past data. Default is False.
        :param `output_towards_future` (bool):          Whether the output sequences come from future data at 
                                                        every time step rather than past data. 
                                                        Default is True for autoregression.
        :param `stacked` (bool):                        If True (default), squeezed columns will be 
                                                        sequence of first feature, 
                                                        then second feature, etc. Otherwise columns will have a
                                                        cascaded arrangement, i.e. features of first time step,
                                                        features of second time step, etc. 
                                                        Only applies to squeezed inputs/outputs.
        :param `extern_input_scaler` (sklearn scaler):  If not None, this scaler will be used to scale the inputs.
                                                        Default is None.
        :param `extern_output_scaler` (sklearn scaler): If not None, this scaler will be used to scale the outputs.
                                                        Default is None.
        :param `scaling` (str):                         Scaling method to use. Default is 'standard'. Other is 'minmax'.


        ### Attributes:

        self.`size` (int): Total number of timesteps in the dataset, after downsampling.
        self.`inscaler` (sklearn.StandardScaler): The standard scaler object, fit to the input data
        self.`outscaler` (sklearn.StandardScaler): The standard scaler object, fit to the output data
        self.`table_in` (numpy matrix): Table of input data, rows are datapoints, columns are features (time steps)
        self.`table_out` (numpy matrix): Table of output data, rows are datapoints, columns are features (time steps)
        self.`shape` (dict): Shape of the dataset object, keys are "in" and "out", 
            which correspond to shapes of numpy matrices representing tabulated inputs and outputs.
        self.`downsampling_rate` (int): Downsampling rate
        self.`in_squeezed` (bool): Whether the input is squeezed (for ANN) or not (for LSTM)
        self.`out_squeezed` (bool): Whether the output is squeezed (for ANN) or not (for LSTM)
        self.`stacked` (bool): Whether the data should be stacked or not
        self.`_scaling` (str): Scaling method to use
        self.`_invec` (numpy array): Array of inputs, after downsampling and scaling
        self.`_outvec` (numpy array): Array of outputs, after downsampling and scaling
        self.`_in_seq_length` (int): Input sequence length (sliding time window length)
        self.`_in_seq_length_ds` (int): Input sequence length (sliding time window length) after downsampling
        self.`_out_seq_length` (int): Output sequence length (sliding time window length)
        self.`_out_seq_length_ds` (int): Output sequence length (sliding time window length) after downsampling
        self.`_in_features` (int):Number of features of input
        self.`_out_features` (int):Number of features of input
        """

        # Make output:
        if output_vec is None:
            output_vec = input_vec.astype(self.DTYPE)
        
        # Reshape inputs and outputs
        if len(input_vec.shape)==1:
            input_vec=input_vec.reshape(-1,1).astype(self.DTYPE)
        if len(output_vec.shape)==1:
            output_vec=output_vec.reshape(-1,1).astype(self.DTYPE)

        if out_features==0:
            out_features = output_vec.shape[-1]

        # Reassure size of data.
        assert len(input_vec.shape)==2 and input_vec.shape[1]==in_features, \
            "All inputs and outputs must be NumData x NumFeatures vectors. "+\
            "Inputs and Outputs must have the same number of rows (datapoints)."
        assert len(output_vec.shape)==2 and output_vec.shape[1]==out_features, \
            "All inputs and outputs must be NumData x NumFeatures vectors. "+\
            "Inputs and Outputs must have the same number of rows (datapoints)."

        # Reassure inputs and outputs have the same size.
        assert input_vec.shape[0]==output_vec.shape[0], \
            "Inputs and Outputs must have the same time length (number of rows)."

        # Reassure type of scaler.
        assert 'standard' in scaling.lower() or 'minmax' in scaling.lower(), \
            "Scaling method must include 'standard' or 'minmax', not case-sensitive."

        
        # Model type and arrangement
        self.in_squeezed = in_squeezed
        self.out_squeezed = out_squeezed
        self.stacked = stacked
        self._scaling = scaling
        self._in_seq_length = in_seq_length
        self._out_seq_length = out_seq_length
        self._input_is_sequence = (in_seq_length > 1)
        self._output_is_sequence = (out_seq_length > 1)
        self.in_features = in_features
        self.out_features = out_features
        self.data_downsampling_rate = data_downsampling_rate
        self.sequence_downsampling_rate = sequence_downsampling_rate

        # Downsampling inputs and outputs
        if data_downsampling_rate > 1:
            idx = np.arange(start=0, stop=input_vec.shape[0], step=data_downsampling_rate).astype(int)
            input_vec = input_vec[idx,:]
            output_vec = output_vec[idx,:]
        self.size = input_vec.shape[0]
        if data_downsampling_rate > 1:
            # int(2**np.round(np.log2(in_seq_length/data_downsampling_rate))) if self._input_is_sequence else 1
            self._in_seq_length_ds = \
                int(np.round(in_seq_length/data_downsampling_rate)) if self._input_is_sequence else 1
            self._out_seq_length_ds = \
                int(np.round(out_seq_length/data_downsampling_rate)) if self._output_is_sequence else 1
        else:
            self._in_seq_length_ds = in_seq_length
            self._out_seq_length_ds = out_seq_length
        


        # Scaling inputs and outputs
        if input_scaling:
            if extern_input_scaler:
                inscaler = extern_input_scaler
            else:
                inscaler = StandardScaler() if 'standard' in scaling.lower() else MinMaxScaler()
                inscaler.fit(input_vec)
            input_vec = inscaler.transform(input_vec).astype(self.DTYPE)
        else:
            inscaler = None

        if output_scaling:
            if extern_output_scaler:
                outscaler = extern_output_scaler
            else:
                outscaler = StandardScaler() if 'standard' in scaling.lower() else MinMaxScaler()
                outscaler.fit(output_vec)
            output_vec = outscaler.transform(output_vec).astype(self.DTYPE)
        else:
            outscaler = None
        
        self.inscaler = inscaler
        self.outscaler = outscaler
        self._invec = input_vec
        self._outvec = output_vec

        ### Tabulating the inputs and outputs
        # Generate tabular input data out of sequential data
        if self._input_is_sequence:
            inputObj = sliding_window(input_vec, self._in_seq_length_ds, self.sequence_downsampling_rate, 
                forward_facing=input_forward_facing, 
                include_current_step=input_include_current_timestep, squeezed=self.in_squeezed, stacked=self.stacked,
                includes_future_data=input_towards_future, dtype=self.DTYPE)
            table_in = inputObj["table"]
            self._in_seq_length_final = inputObj["seq_len_ds"]
        else:
            table_in = input_vec
            self._in_seq_length_final = 1
        if verbose: print("Input Table Shape: ", table_in.shape)

        # Generate tabular output data out of sequential data
        if self._output_is_sequence:
            outputObj = sliding_window(output_vec, self._out_seq_length_ds, self.sequence_downsampling_rate,
                forward_facing=output_forward_facing, 
                include_current_step=output_include_current_timestep, squeezed=self.out_squeezed, stacked=self.stacked,
                includes_future_data=output_towards_future, dtype=self.DTYPE)
            table_out = outputObj["table"]
            self._out_seq_length_final = outputObj["seq_len_ds"]
        else:
            table_out = output_vec
            self._out_seq_length_final = 1
        if verbose: print("Output Table Shape: ", table_out.shape)

        self.table_in = table_in.astype(self.DTYPE)
        self.table_out = table_out.astype(self.DTYPE)
        self.shape = {"in":self.table_in.shape, "out":self.table_out.shape}
        if verbose: print("Dataset constructed successfully.")
    


    def __len__(self):
        return self._invec.size


    def __getitem__(self, key):
        if isinstance(key, slice):
            # get the start, stop, and step from the slice
            return [self[ii] for ii in range(*key.indices(len(self)))]
        elif isinstance(key, int):
            # handle negative indices
            if key < 0:
                key += len(self)
            if key < 0 or key >= len(self):
                raise IndexError("The index (%d) is out of range." % key)
            # get the data from direct index
            return (self._table_in[key,...], self._table_out[key,...])
        else:
            raise TypeError("Invalid argument type.")





def make_squeezed_dataset(hparams:dict, inputs, outputs, **kwargs):
    """Makes a time-series dataset of 2D (squeezed) tensors appropriate to be used by ANN-type deep learning models, using sliding window.
    All the features and timesteps are squeezed to a single feature dimension here.
    This class takes a dictionary of hyperparameters and returns a modified version where "input_size" and "output_size" keys are altered.

    ### Args:
        - `hparams` (dict): Hyperparameters dictionary containing **ALL** of the following keys:
            - `in_seq_len_sec` (float): Input sequence length, in seconds
            - `out_seq_len_sec` (float): Output sequence length, in seconds
            - `data_downsampling` (int): Downsampling rate for generating the dataset. Must be >= 1.
            - `sequence_downsampling` (int): Downsampling rate for generating the sequences. Must be >= 1.
            - `data_sampling_rate_Hz` (float): Sampling rate of the timeseries data, in Hertz.
            - `in_features` (int): Number of input features. Default is 1.
            - `out_features` (int): Number of output features. Default is 1.
        - `inputs` (numpy array): Matrix of pure timeseries inputs, as in (num_data, features)
        - `outputs` (numpy arrays): Matrix of pure timeseries outputs, as in (num_data, features)

    ### Returns:
        - `TabularDataset`: Dataset object, fully preprocessed, usable in a similar format to PyTorch datasets.
        Can be used later for making data loaders, etc.
        - `dict`: Modified dictionary of hyperparameters, also including the `"in_size"` and `"out_size"` keys.
    
    ### Usage:
    `dataset, hparams = make_squeezed_dataset(hparams, inputs, outputs)`
    
    **NOTE** A modified version of the input hyperparams dictionary will also be returned for later use.
    """
    in_window_size_sec = hparams["in_seq_len_sec"]
    out_window_size_sec = hparams["out_seq_len_sec"]
    data_downsampling = hparams.get('data_downsampling') if hparams.get('data_downsampling') else 1
    seq_downsampling = hparams.get('sequence_downsampling') if hparams.get('sequence_downsampling') else 1
    data_sampling_rate_Hz = hparams['data_sampling_rate_Hz']
    
    if not hparams.get('sequence_downsampling') and not hparams.get('data_downsampling') and \
        hparams.get('downsampling'):
        data_downsampling = 1
        seq_downsampling = hparams['downsampling']

    # Why are we doing the following?
    # if in_window_size_sec < out_window_size_sec:
    #     out_window_size_sec = in_window_size_sec

    if in_window_size_sec > 0:
        in_sequence_length = int(in_window_size_sec*data_sampling_rate_Hz)
    else:
        in_sequence_length = 1
    if out_window_size_sec > 0:
        out_sequence_length = int(out_window_size_sec*data_sampling_rate_Hz)
    else:
        out_sequence_length = 1

    # Generating dataset
    dataset = TabularDataset(
        inputs, in_sequence_length, in_features=hparams['in_features'], in_squeezed=True, 
        output_vec=outputs, out_seq_length=out_sequence_length, out_features=hparams['out_features'], 
        out_squeezed=True, data_downsampling_rate=data_downsampling, 
        sequence_downsampling_rate=seq_downsampling, 
        **kwargs)

    hparams["input_size"] = dataset.table_in.shape[-1]
    hparams["output_size"] = dataset.table_out.shape[-1]
    hparams["in_seq_len"] = dataset._in_seq_length_final
    hparams["out_seq_len"] = dataset._out_seq_length_final
    return dataset, hparams





def make_unsqueezed_dataset(hparams:dict, inputs, outputs, **kwargs):
    """Makes a time-series dataset of 3D tensors with shape (batch, timestep, features) appripriate for LSTM-type deep learning models, using sliding window.
    This class takes a dictionary of hyperparameters and returns a modified version where "in_seq_len" and "out_seq_len" keys are altered.

    ### Args:
        - `hparams` (dict): Hyperparameters dictionary containing ALL OF the following keys:
            - `in_seq_len_sec` (float): Input sequence length, in seconds, or zero, if there is no sequence
            - `out_seq_len_sec` (float): Output sequence length, in seconds, or zero, if there is no sequence
            - `data_downsampling` (int): Downsampling rate for generating the dataset. Must be >= 1.
            - `sequence_downsampling` (int): Downsampling rate for generating the sequences. Must be >= 1.
            - `data_sampling_rate_Hz` (float): Sampling rate of the timeseries data, in Hertz.
            - `in_features` (int): Number of input features. Default is 1.
            - `out_features` (int): Number of output features. Default is 1.
        - `inputs` (numpy array): Matrix of pure timeseries inputs, as in (num_data, features)
        - `outputs` (numpy arrays): Matrix of pure timeseries outputs, as in (num_data, features)

    ### Returns:
        - `TabularDataset`: Dataset object, usable in a similar manner to Pytorch datasets.
        Can be used later for making data loaders, etc.
        - `dict`: Modified dictionary of hyperparameters, also including the `"in_seq_len"` and `"out_seq_len"` keys.
    
    ### Usage:
    `dataset, hparams = make_unsqueezed_dataset(hparams, inputs, outputs)`
    
    **NOTE** A modified version of the input hyperparams dictionary will also be returned for later use when 
    constructing the Seq2Dense model.
    """
    in_window_size_sec = hparams["in_seq_len_sec"]
    out_window_size_sec = hparams["out_seq_len_sec"]
    data_sampling_rate_Hz = hparams['data_sampling_rate_Hz']
    data_downsampling = hparams.get('data_downsampling') if hparams.get('data_downsampling') else 1
    seq_downsampling = hparams.get('sequence_downsampling') if hparams.get('sequence_downsampling') else 1
    
    if not hparams.get('sequence_downsampling') and not hparams.get('data_downsampling') and \
        hparams.get('downsampling'):
        data_downsampling = 1
        seq_downsampling = hparams['downsampling']

    if in_window_size_sec != 0:
        in_sequence_length = int(in_window_size_sec*data_sampling_rate_Hz)
    else:
        in_sequence_length = 1
    
    if out_window_size_sec != 0:
        out_sequence_length = int(out_window_size_sec*data_sampling_rate_Hz)
    else:
        out_sequence_length = 1

    # print("Inside make_unsqueezed_dataset:")
    # print("Input sequence length:", in_sequence_length)
    # print("Output sequence length:", out_sequence_length)
    
    dataset = TabularDataset(
        input_vec=inputs, in_seq_length=in_sequence_length, in_features=hparams['in_features'], in_squeezed=False,
        output_vec=outputs, out_seq_length=out_sequence_length, out_features=hparams['out_features'], 
        out_squeezed=True, data_downsampling_rate=data_downsampling, sequence_downsampling_rate=seq_downsampling,
        **kwargs)

    # Sequence length of downsampled data is different, so we have to read it from the dataset object
    in_size = dataset._in_seq_length_final
    out_size = dataset._out_seq_length_final
    hparams['in_seq_len'] = in_size
    hparams['out_seq_len'] = out_size

    return dataset, hparams

