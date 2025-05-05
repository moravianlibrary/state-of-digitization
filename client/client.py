import json

import pandas as pd
import streamlit as st
from sod import (
    DEFAULT_RDCZ_REGISTRY_CONFIG,
    LibId,
    RDczRegistry,
    RelevanceNormalization,
)

# Constants
RDCZ_ISSUE_LINK = "https://registrdigitalizace.cz/rdcz/results;q=id:{ISSUE_ID}"
RDCZ_ISSUE_DISPLAY_REGEX = (
    r"https:\/\/registrdigitalizace\.cz\/rdcz\/results;q=id:(\d+)"
)
RDCZ_RECORD_LINK = (
    "https://registrdigitalizace.cz/rdcz/results;q=titul_id:{RECORD_ID}"
)
RDCZ_RECORD_DISPLAY_REGEX = (
    r"https:\/\/registrdigitalizace\.cz\/rdcz\/results;q=titul_id:(\d+)"
)

NORMALZIATION = RelevanceNormalization.Softmax
SOFTMAX_TEMPERATURE = 0.25


# Initialize registry
registry = RDczRegistry(DEFAULT_RDCZ_REGISTRY_CONFIG)

# Load translations
translations = {}
with open("i18n/cs.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

lib_id_options = [
    translations["lib_ids"][lib_id] for lib_id in LibId._member_names_
]

lib_id_mapping = {
    translations["lib_ids"][lib_id]: lib_id for lib_id in LibId._member_names_
}


def load_file(uploaded_file):
    """Load the file into a DataFrame based on its type."""
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "txt":
        df = pd.DataFrame(
            list(
                line.strip()
                for line in uploaded_file.read().decode("utf-8").splitlines()
                if line.strip()
            ),
            columns=[translations["Values"]],
        )
    elif file_type == "csv":
        df = pd.read_csv(uploaded_file, header=None)
    elif file_type == "xlsx":
        df = pd.read_excel(uploaded_file, header=None)

    if file_type in ["csv", "xlsx"]:
        df.columns = [
            f"{translations["Values"]} {i+1}" for i in range(df.shape[1])
        ]

    return df


def select_row_range(df):
    """Allow the user to select rows from the DataFrame."""
    if df.shape[0] > 1:
        col1, col2 = st.columns(2)

        with col1:
            start_row = st.number_input(
                translations["edit_input_range_placeholder"]["start_row"],
                min_value=0,
                max_value=len(df) - 1,
                value=0,
            )

        with col2:
            end_row = st.number_input(
                translations["edit_input_range_placeholder"]["end_row"],
                min_value=start_row + 1,
                max_value=len(df),
                value=len(df),
            )
    else:
        start_row = 0
        end_row = 1
    return df.iloc[start_row:end_row]


def select_column_range(df):
    """Allow the user to select columns from the DataFrame."""
    if df.shape[1] > 1:
        col1, col2 = st.columns(2)

        with col1:
            start_col_idx = int(
                st.number_input(
                    translations["edit_input_range_placeholder"]["start_col"],
                    min_value=0,
                    max_value=len(df.columns) - 1,
                    value=0,
                )
            )

        with col2:
            end_col_idx = int(
                st.number_input(
                    translations["edit_input_range_placeholder"]["end_col"],
                    min_value=start_col_idx + 1,
                    max_value=len(df.columns),
                    value=len(df.columns),
                )
            )
    else:
        start_col_idx = 0
        end_col_idx = 1
    return df.iloc[:, start_col_idx:end_col_idx]


def create_identifier_columns(df, selected_identifiers):
    """
    Create identifier columns for each column in the DataFrame
    using the selected identifiers.
    """
    expanded_df = pd.DataFrame()
    identifier_columns = []

    for idx, selected_identifier in enumerate(selected_identifiers):
        expanded_df[f"{translations["Value"]} {idx + 1}"] = df.iloc[:, idx]

        # Use the selected identifier for each column
        column_name = f"{translations["Identifier"]} {idx + 1}"
        expanded_df[column_name] = df.iloc[:, idx].apply(
            lambda v: (
                selected_identifier
                or (
                    translations["lib_ids"][LibId.from_value(str(v)).name]
                    if pd.notnull(v)
                    else None
                )
            )
        )
        identifier_columns.append(column_name)

    return expanded_df, identifier_columns


def get_query_results(expanded_df):
    """Query the registry and get the results."""
    result = []

    for _, row in expanded_df.iterrows():
        identifier_values = []

        for idx in range(len(expanded_df.columns) // 2):
            value = row[f"{translations["Value"]} {idx + 1}"]
            identifier_name = row[f"{translations["Identifier"]} {idx + 1}"]
            if pd.notnull(value) and identifier_name:
                identifier_values.append(
                    (LibId[lib_id_mapping[identifier_name]], str(value))
                )

        if identifier_values:
            try:
                response = registry.find_by_identifiers(
                    identifier_values,
                    NORMALZIATION,
                    softmax_temperature=SOFTMAX_TEMPERATURE,
                )

                for relevance, document in response:
                    result.append(
                        {
                            **row,
                            "relevance": relevance,
                            "issue_id": RDCZ_ISSUE_LINK.format(
                                ISSUE_ID=document.issue_id
                            ),
                            "state": document.state.value,
                            "record_id": RDCZ_RECORD_LINK.format(
                                RECORD_ID=document.record_id
                            ),
                            "record_state": [
                                rs.value for rs in document.record_state
                            ],
                            "barcode": document.barcode,
                            "title": document.title,
                            "volume_year": document.volume_year,
                            "volume_number": document.volume_number,
                            "bundle": document.bundle,
                            "control_number": document.control_number,
                            "nbn": document.nbn,
                            "isxn": document.isxn,
                            "signature": document.signature,
                        }
                    )

                if not response:
                    result.append(row)
            except Exception as e:
                st.error(f"Error adding value: {e}")

    return result


def display_results(result):
    """Display the results in a DataFrame."""
    if result:
        resulting_df = pd.DataFrame(result)
        resulting_df = resulting_df.dropna(axis=1, how="all")

        resulting_df = resulting_df.rename(
            columns=translations["results_columns"]
        )

        st.subheader(translations["results_title"])
        st.dataframe(
            resulting_df,
            column_config={
                translations["results_columns"][
                    "issue_id"
                ]: st.column_config.LinkColumn(
                    display_text=RDCZ_ISSUE_DISPLAY_REGEX
                ),
                translations["results_columns"][
                    "record_id"
                ]: st.column_config.LinkColumn(
                    display_text=RDCZ_RECORD_DISPLAY_REGEX
                ),
            },
        )
    else:
        st.warning("No results returned.")


def to_str_or_none(x):
    if pd.isna(x):
        return None
    elif isinstance(x, (int, float)):
        return str(int(x)) if x.is_integer() else str(x)
    return str(x)


def display_df(df, key_prefix=""):
    st.subheader(translations["select_identifiers_title"])

    # Select identifier for all columns
    selected_identifiers = [
        st.selectbox(
            f"{translations["select_column_identifier"]} {idx + 1}",
            options=lib_id_options,
            index=None,
            placeholder=translations["select_column_identifier_placeholder"],
            key=f"{key_prefix}_identifier_{idx}",
        )
        for idx in range(len(df.columns))
    ]

    expanded_df, identifier_columns = create_identifier_columns(
        df, selected_identifiers
    )

    st.write(translations["selected_identifiers"])
    expanded_df = st.data_editor(
        expanded_df,
        column_config={
            column: st.column_config.SelectboxColumn(
                column,
                options=lib_id_options,
                required=False,
            )
            for column in identifier_columns
        },
        hide_index=False,
    )

    if st.button(translations["submit"], key=f"{key_prefix}_submit"):
        result = get_query_results(expanded_df)
        display_results(result)


def main():
    """Main function to execute the app."""

    st.set_page_config(layout="wide")

    st.title(translations["title"])

    tab1, tab2 = st.tabs(
        [translations["file_input_title"], translations["manual_input_title"]]
    )

    with tab1:
        uploaded_file = st.file_uploader(
            translations["file_input_placeholder"], type=["txt", "csv", "xlsx"]
        )

        if uploaded_file is not None:
            df = load_file(uploaded_file)
            df = df.map(to_str_or_none)

            if not df.empty:
                st.write(translations["selected_range"])

                with st.expander(translations["edit_input_range"]):
                    df = select_row_range(df)
                    df = select_column_range(df)

                st.dataframe(df)

                display_df(df, "file_input")

    with tab2:
        manual_input = st.text_area(
            translations["manual_input_info"],
            height=200,
            placeholder=translations["manual_input_placeholder"],
        )
        if manual_input:
            df_manual = pd.DataFrame(
                list(
                    line.strip()
                    for line in manual_input.splitlines()
                    if line.strip()
                ),
                columns=["Values"],
            )

            if not df_manual.empty:
                display_df(df_manual, "manual_input")


if __name__ == "__main__":
    main()
