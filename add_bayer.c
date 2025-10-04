#include <stdint.h>
#include <stdio.h>

void add_bayer(uint8_t *originalMatrix, uint8_t *bayerMatrix, uint8_t *outMatrix, int h, int w, int bayerSize) {
    //计算Bayer最值
    int maxVal = bayerSize * bayerSize - 1;
    
    //打印调试信息
    printf("C开始计算Bayer了！\n");
    printf("bayerSize:%d; h:%d; w:%d; maxVal:%d; \n",bayerSize, h, w, maxVal);

    //打印BayerMatrix
    for (int i = 0;i < maxVal + 1; i++) {
        if (i % bayerSize == bayerSize - 1) printf("[%d]\n",bayerMatrix[i]);
        else printf("[%d],",bayerMatrix[i]);
    }
    
    
    //计算Bayer
    printf("%d\n",originalMatrix[0]);
    for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++) {
            int threshold = bayerMatrix[(y % bayerSize) * bayerSize + (x % bayerSize)] * (255 / maxVal);       
            int location = y * w + x;
            outMatrix[location] = (originalMatrix[location] > threshold) ? 255 : 0;
       //     *(outMatrix + location) = *(originalMatrix + location);
        }
    }
    printf("%d\n",outMatrix[0]);
    
}
