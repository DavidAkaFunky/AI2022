FOLDERNAME="tests_final_public"
END=10

for i in $(seq 1 $END); do        
    echo "$FOLDERNAME/input$i.txt";                          
	time python3 $1 "$FOLDERNAME/input$i.txt"
    echo "-----------------------------";
    echo "";
done