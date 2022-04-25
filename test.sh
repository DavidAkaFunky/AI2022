FOLDERNAME="tests_final_public"
END=12

rm -rf "$1.txt"
for i in $(seq 1 $END); do        
    echo "$FOLDERNAME/input$i.txt" >> "$1.txt";            
    # redirect output with time to folder              
	(time python3 $1 "$FOLDERNAME/input$i.txt") >> "$1.txt" 2>&1 
    echo "-----------------------------" >> "$1.txt";
    echo "" >> "$1.txt";
done