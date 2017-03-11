import bipartite_graphs

start_year = 2005
start_month = 12

end_year = 2006
end_month = 1

year = start_year
month = start_month

file_dates = []

while year*100+month <= 100*end_year+end_month:
    file_date = str(year)+"-"+"0"*(2-len(str(month)))+str(month)
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

bipartite_graph = bipartite_graphs.get_swear_weighted_bipartite_graph_from_files(file_pairs)

