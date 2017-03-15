def file_pairs_from_date_range(start_month, start_year, end_month, end_year):
    year = start_year
    month = start_month

    file_dates = []

    while year * 100 + month <= 100 * end_year + end_month:
        file_date = str(year) + "-" + "0" * (2 - len(str(month))) + str(month)
        file_dates.append(file_date)
        month += 1
        if month > 12:
            month = 1
            year += 1

    file_pairs = [
        {
            "comments_file_path": "./comments/RC_" + date + ".json",
            "threads_file_path": "./submissions/RS_" + date + ".json"
        } for date in file_dates
    ]

    return file_pairs