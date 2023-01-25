# fyers_multiyear_data
Bypassing the historical data request limitation in fyers-apiV2 

When requesting historical data with resolution of "D" , we can only request upto 1 year worth of ohlc data in one request,
and incase this resolution is set to less than "D"(say "60"), we can only request for upto 100 days of data.
This can be a severe limitation when trying to rigrously test your algorithm with multiyear data for multiple insturments.

This program will helps bypass that limitation.

enter the respective credentials in credentials.csv file.
