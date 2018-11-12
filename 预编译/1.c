//说明：如何在预编译语句中使用被预编译的对象值
//define不会替换字符串中的值，所以如果有 #define func(a) "a is a" ,那么func(2) 的到的还是 a is a
//                              如果有 #define func(a) "a is "#a"",那么func(2) 就是 a is 2

//补充说明：这个特性主要就是用来解决 “宏中包含字符串的场景” ， 因为需要区分哪些字符是要被宏替换，哪些是保留原字面意义

//                                如果有 #define func(a) "a is "#a"",那么func(2) 就是 a is 2

#include <stdio.h>
#include <unistd.h>

/* 如果想在字符串里在此引用x，那么需要使用"#x"来替代即可
 *
 *
 * */

#define PRINT_SQU_0(x) do{printf("x -> \"x\" de pingfang = %d \n",x*x);}while(0)
#define PRINT_SQU_1(x) do{printf("x -> "#x" de pingfang = %d \n",x*x);}while(0)
#define PRINT_SQU_2(x) do{printf("x -> #x de pingfang = %d \n",x*x);}while(0)

int main()
{
    PRINT_SQU_0(2); //  x -> "x" de pingfang = 4
    PRINT_SQU_1(2); //  x -> 2 de pingfang = 4
    PRINT_SQU_2(2); //  必须用双引号括起来，不然就是直译为#x

    //while(1) sleep(1);
}
