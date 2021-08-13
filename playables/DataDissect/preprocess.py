import pandas as pd
import streamlit as st

from playables.DataDissect.utils import display_dataset_info, get_func_to_fill
from playables.DataDissect.utils import load_df, save_df, clear_cache, get_feature_info
from playables.DataDissect.preprocess_logic import update_custom_values, fix_missing_values_with, display_cat_preview
from playables.DataDissect.preprocess_logic import convert_datatype_with, get_feature_types, get_cat_feature_values

def fix_missing_values(df, missing_info, feature_type):
    """
    Displays the options for filling in missing/NULL values and calls the
    `fix_missing_values_with()` function to update the dataset

    Args:
    df (Pandas DataFrame)          : The current dataset in the streamlit run
    missing_info (Pandas DataFrame): Info about NULL values in each feature
    feature_type (dict)            : Dictionary of all features' data types
    """
    #Load the streamlit component structure
    container = st.container()
    with container:
        missing_col, fix_options_col = st.columns(2)

    num_features, cat_features, bool_features = feature_type.values()

    #Only move forward if there are actually missing values in the dataset
    if missing_info.sum() != 0:
        with missing_col:
            st.write(f'There are a total of {missing_info.sum()} missing values in the dataset\
                    These are the columns that will be updated:')
            st.write(missing_info)
        #Display available options to user
        with fix_options_col:
            fix_options = ['Do Nothing',
                            'Mean',
                            'Median',
                            'Drop',
                            'Custom'
                            ]
            fix_option = st.radio('How to fill the dataset NULL values?', fix_options)
        #Function to actually fill in the dataset as per the choice and save the dataset
        fix_missing_values_with(df, fix_option.lower(), num_features, cat_features, bool_features)
    else:
        st.write('There are no missing values in the dataset!')

def convert_datatype(df, missing_info, feature_type):
    """
    Displays the current dataset's features and their corresponding data types
    as well as the possible data types that they can be converted to.

    Args:
    df (Pandas DataFrame)          : The current dataset in the streamlit run
    missing_info (Pandas DataFrame): Info about NULL values in each feature
    feature_type (dict)            : Dictionary of all features' data types
    """
    #Continue only if all the missing values have been handled
    if missing_info.sum() != 0:
        st.write('The dataset seems to contain missing/Null values. Please fill the missing values before proceeding further :)')
        return
    #Display urrent features with their data types
    num_features, cat_features, bool_features = feature_type.values()
    all_features = num_features + cat_features + bool_features
    dtypes = df.dtypes.apply(lambda dtype: dtype.name)
    st.write(dtypes)

    conversion_options = {
        'int': ['No Change', 'float', 'str'],
        'float': ['No Change', 'int', 'str'],
        'str': ['No Change', 'int', 'float'],
        'bool': ['No Change', 'int', 'str']
    }
    feature_selections = {}
    #Convert Pandas datatypes to simple string data type name
    feature_types = get_feature_types(dtypes, all_features)

    #Display the current and possible conversion daat types for all features
    with st.form('Datatype Conversion Form'):
        for feature_name in all_features:
            #Create streamlit containers for every part for dynamic UI
            feature_container, type_container, convert_box = st.columns(3)
            type = feature_types[feature_name]
            with feature_container:
                st.write(f'Feature Name: **{feature_name}**')
                st.write('\n')
                st.write('\n')
            with type_container:
                st.write(f'Current Datatype: ** *{type}* **')
                st.write('\n')
                st.write('\n')
            with convert_box:
                type_select = st.selectbox('Select new datatype:', conversion_options[type], key=feature_name)
                feature_selections[feature_name] = type_select

        #Gives warning and then updates the feature data-types as selected by the user
        st.write('This step is ir-reversible. Please check the selections and click Update')
        update = st.form_submit_button('Update Dataset')
        if update:
            convert_datatype_with(df, feature_selections, feature_types, all_features)

def handle_categorical(df, feature_type):
    """
    Gives user the choiceto select the type of encoding to use for each categorical variable
    and whether to use custom or default values for it

    Args:
    df (Pandas DataFrame)          : The current dataset in the streamlit run
    feature_type (dict)            : Dictionary of all features' data types
    """
    #Get all the categorical features' names from the dict
    _, cat_features, _ = feature_type.values()

    #Return if there are no categorical features present in the dataset
    if len(cat_features) == 0:
        st.write('All categorical data seems to have been handled well ;)')
        return

    #Convert the categorical features to one-hot/label encoded form as selected by user
    st.write('Please select the desired option for the categorical features present in the dataset.')
    st.write('You can uncheck the **USE DEFAULTS** checkbox to enter custom labels for label encoding on the next page')

    encoding_choices = ['No Change', 'Label Encoding', 'One-Hot Encoding']
    feature_choice = {}
    feature_values = {}
    use_defaults = {}

    placeholder = st.empty()
    #Boolean to keep track of the first and preview screen
    first_screen = False

    #If user has never been or isn't currently on preview screen, mark the flag as first screen
    if 'preview_status' not in st.session_state:
        first_screen = True
    else:
        if st.session_state['preview_status'] == False:
            first_screen = True

    #Renders the first screen and display the features and user options
    if first_screen:
        with placeholder.form('Handling Categorical'):
            for feature_name in cat_features:
                feature_choice_col, feature_values_col = st.columns(2)

                with feature_choice_col:
                    #Display the feature name along with the encoding and default choices
                    st.write(f'Feature Name: **{feature_name}**')
                    feature_choice[feature_name] = st.radio('Select your choice', encoding_choices, key=feature_name)
                    use_defaults[feature_name] = st.checkbox(
                        'Use default values for encoding \n \
                        (Uncheck this to provide custom encodings on the next page)',
                        key=feature_name+'default_encoding')

                with feature_values_col:
                    #Displays the unique values present in the feature and their distribution
                    st.write('Value distribution of feature:')
                    feature_values[feature_name] = get_cat_feature_values(df, feature_name)
                    st.write(feature_values[feature_name])

            #Display the warning for an issue with the current version of streamlit
            st.warning('On clicking the Preview button, you might receive a \'Bad Message\' warning.\
                It is a bug in the current release of Streamlit and will be fixed in the future update.\
                Simply click Done and continue with your work :)')

            preview_button = st.form_submit_button('Preview')
    else:
        preview_button = True

    #If it's the preview screen or the user clicks it explicitly, render the next screen
    if preview_button:
        st.session_state['preview_status'] = True
        placeholder.empty()
        display_cat_preview(df, encoding_choices, feature_choice, feature_values, use_defaults)

def pre_process_data(df):
    """Displays the pre-processing options and acts as a wrapper function"""

    df = load_df(curr_df=df)
    #Display dataset sample without any summary and profiling report
    display_dataset_info(df, without_summary=True, profiling=False, subheader='Current Dataset:')
    options_available, option_description = st.columns([1,2])
    #Get the info about NULL values as well as data types of all features
    missing_info, feature_type = get_feature_info(df)

    with options_available:
        options = ['', 'Fix Missing Values', 'Convert DataType', 'Handle Categorical Data']
        todo = st.radio('Options Available:', options)

    #Execute the individual feature depending upon the user choice
    if todo == options[1]:
        with option_description:
            st.write("\n\n\n\n")
            st.write('Null/Missing values can be harmful to the modelling.\
                      Use Mean, Median or Mode to fill up the missing values!')
        fix_missing_values(df, missing_info, feature_type)
    elif todo == options[2]:
        with option_description:
            st.write("\n\n\n\n")
            st.write('Sometimes, we might have to convert the datatype of certain\
            variables to use them.')
        convert_datatype(df, missing_info, feature_type)
    elif todo == options[3]:
        with option_description:
            st.write("\n\n\n\n")
            st.write('Convert categorical data into its numeric counterpart')
        handle_categorical(df, feature_type)
