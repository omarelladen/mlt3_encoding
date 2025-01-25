#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h> 

#define DATA_MAX_SIZE 11

int8_t* mlt3(bool signal[])
{
  int8_t *mlt3_data = (int8_t*)malloc(DATA_MAX_SIZE * sizeof(int8_t));

  if (mlt3_data == NULL) {
      printf("malloc error\n");
      exit(1);
  }

  int8_t data_out_ant = signal[0];  
  mlt3_data[0] = data_out_ant;

  int8_t sign = -1; 
  if(data_out_ant == 1)
    sign = 1;

  for(int64_t i=1; i<DATA_MAX_SIZE; i++)
  {
    if(signal[i] == 0)
    {
      //data_out_ant = data_out_ant;
    }
    else if(data_out_ant != 0 && signal[i] == 1)
    {
      data_out_ant = 0;
    }
    else if(data_out_ant == 0 && signal[i] == 1)
    {
      sign *= -1;
      data_out_ant = sign;
    }

    mlt3_data[i] = data_out_ant;
  }

  return mlt3_data;
}
int main()
{
  bool signal[DATA_MAX_SIZE] = {0,1,0,0,1,1,1,0,0,1,1};
  int64_t data_size = sizeof(signal) / sizeof(signal[0]);
  printf("size: %d\n", data_size);
  for(int64_t i=0; i<data_size; i++)
    printf("%d ", signal[i]);

  printf("\n");

  int8_t *mlt3_data = mlt3(signal);
  for(int64_t i=0; i<data_size; i++)
    printf("%d ", mlt3_data[i]);


  free(mlt3_data);


  printf("\n\nOmar El Laden\n");
  return 0;
  
}
