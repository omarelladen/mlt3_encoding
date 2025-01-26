#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

// Return the data after MLT-3 transformation
int8_t* mlt3(bool data[], int64_t data_size)
{
  // Allocate vector for the mlt3
  int8_t *mlt3_data = (int8_t*)malloc(data_size * sizeof(int8_t));
  if (mlt3_data == NULL)
  {
      printf("Error allocating memmory for mlt3\n");
      exit(1);
  }

  // First output is the same
  int8_t data_out = data[0];  
  mlt3_data[0] = data_out;

  // Sign initalization
  int8_t sign = -1; 
  if(data_out == 1)
    sign = 1;

  // MLT-3
  for(int64_t i=1; i<data_size; i++)
  {
    if(data_out != 0 && data[i] == 1)
      data_out = 0;
    else if(data_out == 0 && data[i] == 1)
    {
      sign *= -1;
      data_out = sign;
    }
    // else if(data[i] == 0)
    // {
    //   //data_out = data_out;
    // }

    mlt3_data[i] = data_out;
  }


  return mlt3_data;
}

int main()
{
  // Open text file
  FILE *file = fopen("message.txt", "r"); // windows may need rb
  if (file == NULL)
  {
      perror("Error opening the message.txt file");
      return 1;
  }

  // Get file size 
  fseek(file, 0, SEEK_END);
  int64_t text_file_size = ftell(file); //in bytes (with LF)
  fseek(file, 0, SEEK_SET); // return to the beggining of the file

  // Allocate vector for the text
  unsigned char *file_char_data = malloc(text_file_size);
  if (file_char_data == NULL)
  {
      perror("Error allocating memmory for file content");
      fclose(file);
      return 1;
  }

  // Put the text in the vector
  int64_t bytes_lidos = fread(file_char_data, 1, text_file_size, file);
  if (bytes_lidos != text_file_size)
  {
      perror("Error reading the file");
      free(file_char_data);
      fclose(file);
      return 1;
  }

  // Print vector content
  printf("File text without LF:\n");
  for (int64_t i = 0; i < text_file_size-1; i++) // -1 (last is LF)
    printf("%c", (file_char_data[i]));  // each char


  // Allocate bin vector for the bin vector
  bool *bin_data = (bool*)malloc(sizeof(bool)*text_file_size); // bool has 1Byte 
  if (bin_data == NULL)
  {
      perror("Error allocating memmory for bin data");
      fclose(file);
      return 1;
  }

  // Put the data in binary
  int64_t data_pos_cont=0;
  for (int64_t i = 0; i < text_file_size-1/*last byte is LF*/; i++) // each char (byte)
    for (int8_t j = 7; j >= 0; j--) // each bit in the byte
      bin_data[data_pos_cont++] = (file_char_data[i] >> j) & 1;

  // rm original data
  free(file_char_data);
  fclose(file);

  // Print binary data
  printf("\n\nData:\n");
  int64_t cont_8=0;
  for(int64_t i=0; i<data_pos_cont; i++)
  {
    printf("%d ", bin_data[i]);

    if(cont_8++ == 7)
    {
      printf("   ");
      cont_8 = 0;
    }
  }
  
  
  // Print data after MLT-3 transformation
  printf("\n\nMLT-3:\n");
  cont_8=0;
  int8_t *mlt3_data = mlt3(bin_data, data_pos_cont);
  for(int64_t i=0; i<data_pos_cont; i++)
  {
    printf("%d ", mlt3_data[i]);

     if(cont_8++ == 7)
    {
      printf("   ");
      cont_8 = 0;
    }
  }
  


  free(bin_data);
  free(mlt3_data);

  printf("\n");

  // printf("\n\nstd bool type size: %d byte\n", sizeof(bool));
  // printf("text size: %d bits\n", data_pos_cont);


  return 0;
}
