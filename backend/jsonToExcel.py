import pandas as pd

def convert_to_excel(person_result, company_results, company):
    # Convert person_result to DataFrame
    person_data = []
    for full_title, categories in person_result.items():
        for category, results in categories.items():
            for result in results:
                person_data.append({
                    "Name and Role": full_title.split(", ")[1], 
                    "Category": category,
                    "Title": result["title"],
                    "Description": result["desc"],
                    "Link": result["link"],
                })

    person_df = pd.DataFrame(person_data)

    # Convert company_results to DataFrame
    company_data = []
    for category, results in company_results.items():
        for result in results:
            company_data.append({
                "Category": category,
                "Title": result["title"],
                "Description": result["desc"],
                "Link": result["link"],
            })

    company_df = pd.DataFrame(company_data)

    # Export DataFrames to Excel
    output_file = "output.xlsx"
    with pd.ExcelWriter(output_file) as writer:
        person_df.to_excel(writer, sheet_name="Person Results", index=False)
        company_df.to_excel(writer, sheet_name="Company Results", index=False)

    print(f"Data has been exported to {output_file}")

    return output_file