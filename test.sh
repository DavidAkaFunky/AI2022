FOLDERNAME="tests_final_public"
END=10

for i in $(seq 1 $END); do        
    echo "$FOLDERNAME/input$i.txt";                          
	time python3 numbrix.py "$FOLDERNAME/input$i.txt"
    echo "-----------------------------";
    echo "";
done