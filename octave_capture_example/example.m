data = csvread("2020-03-10_15_10_32.csv");

plot(data(:,1),data(:,2))

datafft = csvread("2020-03-10_15_10_32fft.csv");
figure
plot(datafft(:,2),datafft(:,1))

ch1 = data(:,2);


figure

ch1_fft = fft(ch1);
plot(abs(ch1_fft));