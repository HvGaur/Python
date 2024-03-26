// LINEAR CONVOLUTION
// #include <stdio.h>
// #include<math.h>

// float y[10];

// int main(){
//     int x[4] = {1,2,3,4};
//     int h[4] = {2,2,2,2};
//     int xlen = 4;
//     int hlen = 4;
//     int N = xlen + hlen - 1;
//     int n,k;
//     for(n=0;n<N;n++)
//     {
//         y[n] = 0;
//         for(k=0;k<hlen;k++)
//         {
//             if(((n-k)>=0)&&((n-k)<xlen))
//                 y[n] = y[n] + h[k]*x[n-k] ;
//         }
//         printf("%f\t", y[n]);
//     }
// }

// ---------------------------------------------------

// CIRCULAR CONVOLUTION
// #include<stdio.h>
// #include<math.h>
// float y[10];
// int main(){
//     int x[5] = {1,2,3,4,5};
//     int h[5] = {2,1,3,4,5};
//     int N = 5;
//     int n,k,i;
//     for(n = 0; n < N; n++)
//     {
//         y[n] = 0;
//         for(k = 0; k < N; k++)
//         {
//             i = (n-k)%N;
//             if(i<0)
//                 i = i + N;
//             y[n] = y[n] + h[k]*x[i];
//         }
//         printf("%f\t", y[n]);
//     }
// }

// ---------------------------------------------------

// DFT
// #include<stdio.h>
// #include<math.h>
// float y[16];
// int main()
// {
//     float x[4] = {1,3,2,5};
//     int xlen = 4;
//     float w;
//     int n, k, k1;
//     int N = 4;
//     for(k=0;k<2*N;k=k+2)
//     {
//         y[k] = 0;
//         y[k+1] = 0;
//         k1 = k/2;
//         for(n = 0; n < xlen; n++)
//         {
//             w = -2*3.14*k1*n/N;
//             y[k] = y[k] + x[n]*cos(w);
//             y[k+1] = y[k+1] + x[n]*sin(w);
//         }
//         printf("%f + i%f\n", y[k],y[k+1]);
//     }
// }

// ---------------------------------------------------

// IMPULSE RESPONSE
#include<stdio.h>



int main(){
    float x[60], y[60];
    float a1,a2,b0,b1,b2;
    a1 = -1.1430; a2 = 0.4128;
    b0 = 0.0675; b1 = 0.1349; b2 = 0.0675;
    int i, j;
    int N = 20;
    x[0] = 1;
    for(i = 1; i < N; i++)
    {
        x[i] = 0;
    }
    for(j = 0; j < N; j++)
    {
        y[j] = b0*x[j];
        if(j>0)
            y[j] = y[j] + b1*x[j-1] - a1*y[j-1];
        if((j-1)>0)
            y[j] = y[j] + b2*x[j-2] - a2*y[j-2];
        printf("%f\t", y[j]);
    }
}