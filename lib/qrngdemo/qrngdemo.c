#include <stdio.h> // getchar()
#include "libQRNG.h"

#define QRNG_USERNAME_LENGTH 64+1
#define QRNG_PASSWORD_LENGTH 64+1

#define ARRAY_SIZE 5
#define PASSWORD_LENGTH 12+1

int main(int argc, char* argv[])
{
	char qrng_username[QRNG_USERNAME_LENGTH];
	char qrng_password[QRNG_PASSWORD_LENGTH];

	int retcode, actual_count;

	char byte_array[ARRAY_SIZE];
	double double_value;
	double double_array[ARRAY_SIZE];
	int int_value;
	int int_array[ARRAY_SIZE];
	char generated_password[PASSWORD_LENGTH];
	const char tobeused_password_chars[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

	int use_ssl = 0;
	int i, array_index;

	printf("This demo program shows how to use the various functions offered by libQRNG.\n");
	printf("It tries to connect to the QRNG service and execute all these functions.\n");
	printf("\nusing QRNG library: %s\n\n", qrng_libQRNG_version);

	printf("Please enter your username and password now.\nIf you do not have any account for the QRNG service yet,\nplease register first at http://qrng.physik.hu-berlin.de/register/\n");
	printf("Username: ");
	fgets(qrng_username, QRNG_USERNAME_LENGTH, stdin);
	printf("Password: ");
	fgets(qrng_password, QRNG_PASSWORD_LENGTH, stdin);

	/* 2 runs: W/O and W/ SSL */
	for (i = 0; i <= 1; i++) {
		printf("\n-------------------------------------------\n");
		/* connect */
		if (use_ssl) {
			retcode = qrng_connect_SSL(qrng_username, qrng_password);
			if (retcode != 0) {
				printf("ERROR: Failed to connect to QRNG service using SSL: %s\n", qrng_error_strings[retcode]);
				if (retcode == QRNG_ERR_FAILED_TO_INIT_SSL) {
					printf("The library failed to initialise the SSL part.\n");
					printf("If you want to use SSL, make sure you installed the following things:\n");
					printf("a) Windows binaries of the OpenSSL Library\n");
					printf("     get it from http://www.slproweb.com/products/Win32OpenSSL.html\n");
					printf("b) Visual C++ 2008 Redistributable Package (x86)\n");
					printf("     (needed for the OpenSSL Library binaries)\n");
					printf("     get it from http://www.microsoft.com/downloads/details.aspx?familyid=9B2DA534-3E03-4391-8A4D-074B9F2BC1BF\n");
				}
				break;
			}
			printf("Successfully connected to QRNG service using SSL\n");
		} else {
			retcode = qrng_connect(qrng_username, qrng_password);
			if (retcode != 0) {
				printf("ERROR: Failed to connect QRNG service: %s\n", qrng_error_strings[retcode]);
				break;
			}
			printf("Successfully connected to QRNG service\n\n");
		}

		/* execute libQRNG functions */
		/* byte */
		retcode = qrng_get_byte_array((char*)& byte_array, ARRAY_SIZE, & actual_count);
		if (retcode) {
			printf("ERROR: Failed to execute qrng_get_byte_array(), error: %s", qrng_error_strings[retcode]);
		} else {
			printf("Executed qrng_get_byte_array(), got %d bytes:\n", actual_count);
			for (array_index = 0; array_index < actual_count; array_index++) {
				printf("Byte %d: %d%d%d%d%d%d%d%d\n", array_index,
					byte_array[array_index] & 0x1 ? 1 : 0,
					byte_array[array_index] & 0x2 ? 1 : 0,
					byte_array[array_index] & 0x4 ? 1 : 0,
					byte_array[array_index] & 0x8 ? 1 : 0,
					byte_array[array_index] & 0x10 ? 1 : 0,
					byte_array[array_index] & 0x20 ? 1 : 0,
					byte_array[array_index] & 0x40 ? 1 : 0,
					byte_array[array_index] & 0x80 ? 1 : 0
				);
			}
		}
		printf("\n");
		/* double */
		retcode = qrng_get_double((double*)& double_value);
		if (retcode) {
			printf("ERROR: Failed to execute qrng_get_double(), error: %s", qrng_error_strings[retcode]);
		} else {
			printf("\nExecuted qrng_get_double(), got double value: %lf:\n", double_value);
		}

		retcode = qrng_get_double_array((double*)& double_array, ARRAY_SIZE, & actual_count);
		if (retcode) {
			printf("ERROR: Failed to execute qrng_get_double_array(), error: %s", qrng_error_strings[retcode]);
		} else {
			printf("\nExecuted qrng_get_double_array(), got %d doubles:\n", actual_count);
			for (array_index = 0; array_index < actual_count; array_index++) {
				printf("Double %d: %lf\n", array_index, double_array[array_index]);
			}
		}
		/* int */
		retcode = qrng_get_int((int*)& int_value);
		if (retcode) {
			printf("ERROR: Failed to execute qrng_get_int(), error: %s", qrng_error_strings[retcode]);
		} else {
			printf("\nExecuted qrng_get_int(), got int value: %d:\n", int_value);
		}

		retcode = qrng_get_int_array((int*)& int_array, ARRAY_SIZE, & actual_count);
		if (retcode) {
			printf("ERROR: Failed to execute qrng_get_int_array(), error: %s", qrng_error_strings[retcode]);
		} else {
			printf("\nExecuted qrng_get_int_array(), got %d ints:\n", actual_count);
			for (array_index = 0; array_index < actual_count; array_index++) {
				printf("Int %d: %d\n", array_index, int_array[array_index]);
			}
		}
		/* password */
		retcode = qrng_generate_password((const char*) & tobeused_password_chars, (char*) & generated_password, sizeof(generated_password));
		if (retcode) {
			printf("ERROR: Failed to execute qrng_generate_password(), error: %s", qrng_error_strings[retcode]);
		} else {
			printf("\nExecuted qrng_generate_password(), got random password: %s\n", generated_password);
		}

		/* disconnect */
		qrng_disconnect();
		use_ssl = !use_ssl;
		printf("\n\n");
	}

	printf("press return to exit...");
	/* program blocked (waiting for user input) */
	getchar();

	return 0;
}
