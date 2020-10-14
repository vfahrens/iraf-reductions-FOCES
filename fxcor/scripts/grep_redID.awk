BEGIN{FS="|"}/fcs_/&&($24==redmineid){print $0}
