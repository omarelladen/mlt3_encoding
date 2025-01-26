#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

// Return the data after MLT-3 encoding
int8_t* mlt3(bool data[], int64_t data_size)
{
  // Allocate vector for the mlt3
  int8_t *mlt3_data = (int8_t*)malloc(data_size * sizeof(int8_t));
  if (mlt3_data == NULL)
  {
      printf("Error allocating memmory for mlt3\n");
      exit(1);
  }

  // First output signal is the same
  int8_t signal_out = data[0];  
  mlt3_data[0] = signal_out;

  // Sign initalization
  int8_t sign = -1; 
  if(signal_out == 1)
    sign = 1;

  // MLT-3 encoding to mlt3_data
  for(int64_t i=1; i<data_size; i++)
  {
    // Check current data and last signal to get the next signal value
    if(data[i] == 1)  
    {
      if(signal_out == 0)
      {    
        sign *= -1;
        signal_out = sign;
      }
      else
        signal_out = 0;
    }
    mlt3_data[i] = signal_out;
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

  int64_t bin_data_size = text_file_size * 8; // 8 bool for each char (1 Byte)


  // Allocate vector for the text
  unsigned char *file_char_data = (unsigned char*)malloc(text_file_size * sizeof(unsigned char));
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
  printf("Text:\n");
  for (int64_t i = 0; i < text_file_size-1; i++) // -1 (last is LF)
    printf("%c", (file_char_data[i]));  // each char


  // Allocate bin vector for the bin vector
  bool *bin_data = (bool*)malloc(sizeof(int8_t) * bin_data_size);
  if (bin_data == NULL)
  {
      perror("Error allocating memmory for bin data");
      fclose(file);
      return 1;
  }

  // Put the data in binary
  int64_t data_pos_cont=0;
  for (int64_t i = 0; i < text_file_size; i++) // each char (byte)
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


  // Print data after MLT-3 encoding
  printf("\n\nMLT-3:\n");
  cont_8=0;
  int8_t *mlt3_data = mlt3(bin_data, bin_data_size);
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

  return 0;
}