for i in *.zip; do
    mkdir ${i::-4}folder
    cs=${i:7:7}
    for j in ${cs}*; do
        echo $j
        mv "${j}" ${i::-4}folder
    done
    echo eeeeeee
done