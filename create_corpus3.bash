#$1 プロジェクト名
echo "=== $1 ==="
#$2 パス名
echo "=== $2 ==="

for path in $(find $2 -name \*.c)
do
    ./a.out < $path |python3 tokenizer.py  |python3 ngram_corpus3.py $1 $path
done    