#include <stdio.h>

int main(void) {
    char ch;
    int state = 0;
    /* 状態：初期状態 = 0， 
        ダブルクォーテーション内 = 1，
        ダブルクォーテーション内でエスケープ中 = 10,
        シングルクォーテーション内 = 2,
        シングルクォーテーション内 でエスケープ中 = 20,
        コメントの始まりの可能性 = 3,
        C の伝統的なコメント内 = 30,
        C の伝統的なコメントの終わりの可能性 = 31,
        C++ のコメント内 = 300
    */
    /* 読み込みファイルの終端まで文字を読み取り表示する */
    while (( ch = getchar()) != EOF ) {
        if ( state == 0 ){
            if ( ch == '\"' ){
                state = 1;
                putchar('\t');
                putchar(ch);
            }
            else if ( ch == '\'' ){
                state = 2;
                putchar('\t');
                putchar(ch);
            }
            else if ( ch == '/' ){
                state = 3;
            }
            else{
                putchar(ch);
            }
            continue;
        }

        if ( state == 1 ){
            putchar(ch);
            if( ch =='\\' ){
                state = 10;
            }
            else if ( ch == '\"' ){
                putchar('\t');
                state = 0;
            }
            continue;
        }

        if ( state == 2 ){
            putchar(ch);
            if( ch =='\\' ){
                state = 20;
            }
            else if ( ch == '\'' ){
                putchar('\t');
                state = 0;
            }
            continue;
        }

        if ( state == 10 ){
            putchar(ch);
            state = 1;
            continue;
        }

        if ( state == 20 ){
            putchar(ch);
            state = 2;
            continue;
        }

        if ( state == 3 ){
            if ( ch == '*' ){
                state = 30;
            }
            else if ( ch == '/' ){
                state = 300;
            }
            else{
                putchar('/');
                putchar(ch);
                if ( ch == '\"' ){
                    state = 1;
                }
                else if ( ch == '\'' ){
                    state = 2;
                }
                else {
                    state = 0;
                }
            }
            continue;
        }

        if ( state == 30 ){
            if ( ch == '*' ){
                state = 31;
            }
            continue;
        }

        if ( state == 31 ){
            if ( ch == '/' ){
                state = 0;
            }
            else{
                state = 30;
            }
            continue;
        }

        if ( state == 300 ){
            if ( ch == '\n' ){
                state = 0;
            }
            continue;
        }
    }
    return 0;

}