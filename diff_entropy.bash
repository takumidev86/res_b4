#$1 パス名
echo "=== $1 ==="
#$2 古いハッシュ値
echo "=== $2 ==="

#$3 新しいハッシュ値
echo "=== $3 ==="

for path in $(find $1 -name \*.c)
do
    git diff -U0 -w  $2 $3 -- $path |python3 /home/krst8639/krst8/Desktop/kuri-repo/research/preprocessing/diff.py $path
done    