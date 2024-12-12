# app.py
import sqlite3
import streamlit as st
import pandas as pd

# Database setup
DB_NAME = "stories_methods.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS methods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        partner TEXT,
        contact_person TEXT,
        email TEXT,
        task TEXT,
        method_type TEXT,
        method_name TEXT,
        objective TEXT,
        maturity TEXT,
        part_of_method TEXT,
        unique_id TEXT,
        category TEXT,
        scale TEXT,
        documentation TEXT,
        cost_time TEXT,
        accessibility TEXT,
        interoperability TEXT,
        relevance TEXT,
        beyond_applicability TEXT,
        inputs TEXT,
        input_scale TEXT,
        input_details TEXT,
        outputs TEXT,
        output_scale TEXT,
        output_details TEXT,
        comments TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_method(entry):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO methods (
        partner, contact_person, email, task, method_type, method_name, objective,
        maturity, part_of_method, unique_id, category, scale, documentation,
        cost_time, accessibility, interoperability, relevance, beyond_applicability,
        inputs, input_scale, input_details, outputs, output_scale, output_details, comments
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, entry)
    conn.commit()
    conn.close()

def get_methods():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM methods")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_method(method_id, updated_entry):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE methods SET
        partner = ?, contact_person = ?, email = ?, task = ?, method_type = ?, method_name = ?, 
        objective = ?, maturity = ?, part_of_method = ?, unique_id = ?, category = ?, scale = ?, 
        documentation = ?, cost_time = ?, accessibility = ?, interoperability = ?, relevance = ?, 
        beyond_applicability = ?, inputs = ?, input_scale = ?, input_details = ?, outputs = ?, 
        output_scale = ?, output_details = ?, comments = ? WHERE id = ?
    """, tuple(updated_entry) + (method_id,))
    conn.commit()
    conn.close()

def delete_method(method_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM methods WHERE id = ?", (method_id,))
    conn.commit()
    conn.close()

# Streamlit app
def main():
    st.title("StoRIES Method Management")
    st.sidebar.title("Navigation")
    options = ["View Methods", "Add Method", "Update Method", "Delete Method"]
    choice = st.sidebar.selectbox("Choose an action", options)

    if choice == "View Methods":
        st.subheader("All Methods")
        methods = get_methods()
        df = pd.DataFrame(methods, columns=[
            "ID", "Partner", "Contact Person", "Email", "Task", "Method Type", "Method Name",
            "Objective", "Maturity", "Part Of Method", "Unique ID", "Category", "Scale",
            "Documentation", "Cost & Time", "Accessibility", "Interoperability", 
            "Relevance", "Beyond Applicability", "Inputs", "Input Scale", 
            "Input Details", "Outputs", "Output Scale", "Output Details", "Comments"
        ])
        st.dataframe(df)

    elif choice == "Add Method":
        st.subheader("Add a New Method")
        with st.form("add_form"):
            partner = st.text_input("Partner", "Enter the name of the partner organization")
            contact_person = st.text_input("Contact Person", "First Name Last Name")
            email = st.text_input("Email", "firstname.lastname@partner.xy")
            task = st.text_input("Task", "Choose one of T1.2, T1.3, T1.4, T2.2, T2.4")
            method_type = st.selectbox("Method Type", ["Model", "Experiment", "Manufacturing"])
            method_name = st.text_input("Method Name", "Provide a very concise and unique description")
            objective = st.text_area("Objective", "Describe the main purpose of the method within the project")
            maturity = st.selectbox("Maturity", [
                "Established method", 
                "Method under development outside StoRIES available from mm/yyyy",
                "Method under development in StoRIES in T1.x available from mm/yyyy"
            ])
            part_of_method = st.text_input("Part Of Method", "Provide the unique_id if applicable")
            unique_id = st.text_input("Unique ID", "Enter the unique ID assigned to this method")
            category = st.text_input("Category", "Name of the folder on the project SharePoint")
            scale = st.selectbox("Scale", ["device", "component", "macrohomogeneous local", "meso", "LRE", "Atomistic"])
            documentation = st.text_input("Documentation", "Provide a link to detailed documentation")
            cost_time = st.text_area("Cost & Time", "Specify time required based on method type")
            accessibility = st.text_area("Accessibility", "Describe availability or restrictions")
            interoperability = st.text_area("Interoperability", "Highlight compatibility and complexity")
            relevance = st.text_area("Relevance", "List relevant use cases or applications")
            beyond_applicability = st.text_area("Beyond Applicability", "Mention other use cases")
            inputs = st.text_area("Inputs", "List all inputs required")
            input_scale = st.text_input("Input Scale", "Specify the scale of each input")
            input_details = st.text_area("Input Details", "Provide additional details about the inputs")
            outputs = st.text_area("Outputs", "List all outputs produced")
            output_scale = st.text_input("Output Scale", "Specify the scale of each output")
            output_details = st.text_area("Output Details", "Provide additional details about the outputs")
            comments = st.text_area("Comments", "Add any additional comments or notes")
            submitted = st.form_submit_button("Add Method")
        
        if submitted:
            add_method((
                partner, contact_person, email, task, method_type, method_name, objective, maturity, 
                part_of_method, unique_id, category, scale, documentation, cost_time, accessibility, 
                interoperability, relevance, beyond_applicability, inputs, input_scale, input_details, 
                outputs, output_scale, output_details, comments
            ))
            st.success("Method added successfully!")

    elif choice == "Update Method":
        st.subheader("Update an Existing Method")
        methods = get_methods()
        method_id = st.selectbox("Select Method ID to Update", [m[0] for m in methods])
        method = next(m for m in methods if m[0] == method_id)
        with st.form("update_form"):
            updated_values = [
                st.text_input("Partner", method[1]),
                st.text_input("Contact Person", method[2]),
                st.text_input("Email", method[3]),
                st.text_input("Task", method[4]),
                st.selectbox("Method Type", ["Model", "Experiment", "Manufacturing"], index=["Model", "Experiment", "Manufacturing"].index(method[5])),
                st.text_input("Method Name", method[6]),
                st.text_area("Objective", method[7]),
                st.text_input("Maturity", method[8]),
                st.text_input("Part Of Method", method[9]),
                st.text_input("Unique ID", method[10]),
                st.text_input("Category", method[11]),
                st.text_input("Scale", method[12]),
                st.text_input("Documentation", method[13]),
                st.text_area("Cost & Time", method[14]),
                st.text_area("Accessibility", method[15]),
                st.text_area("Interoperability", method[16]),
                st.text_area("Relevance", method[17]),
                st.text_area("Beyond Applicability", method[18]),
                st.text_area("Inputs", method[19]),
                st.text_input("Input Scale", method[20]),
                st.text_area("Input Details", method[21]),
                st.text_area("Outputs", method[22]),
                st.text_input("Output Scale", method[23]),
                st.text_area("Output Details", method[24]),
                st.text_area("Comments", method[25]),
            ]
            submitted = st.form_submit_button("Update Method")
        
        if submitted:
            update_method(method_id, updated_values)
            st.success("Method updated successfully!")

    elif choice == "Delete Method":
        st.subheader("Delete a Method")
        methods = get_methods()
        method_id = st.selectbox("Select Method ID to Delete", [m[0] for m in methods])
        if st.button("Delete Method"):
            delete_method(method_id)
            st.success("Method deleted successfully!")

if __name__ == "__main__":
    init_db()
    main()
