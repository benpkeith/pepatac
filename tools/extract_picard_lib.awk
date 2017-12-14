# This script reads a picard metrics file and parses out
# the ESTIMATED_LIBRARY_SIZE field. run it like:
# awk -F'\t' -f extract_picard_lib.awk metrics_file.txt

/## METRICS CLASS/ { 
  for(i=1; i<=2; i++) {
    getline;
    c=-1;
    # Find the column of interest
    for(j=1; j<=10; j++) { 
      if ($j == "ESTIMATED_LIBRARY_SIZE") c=j 
    }

    if (c != -1) {
    while(getline && $0 != "") {
      #getline;
      if ($c == "") {
        #print "Unknown"
      } else {
      }
        # Aggregate library size for different read groups
        t = t + $c
    }
    }
  }
  print t
}