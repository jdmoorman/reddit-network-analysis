clc
close all
clear all

individual_swears_monthly = import_individual_swears_monthly('individual_swears_monthly.csv');
monthly_swear_and_word_totals = import_monthly_swear_and_word_totals('monthly_swear_and_word_totals.csv');

swears = individual_swears_monthly.Properties.VariableNames;
swears(1) = []; % Get rid of month

months = individual_swears_monthly.('month');
n_months = size(months,1);
start_month = datenum(months{1});
end_month = datenum(months{n_months});
months = linspace(start_month, end_month, n_months);

word_counts = monthly_swear_and_word_totals.('words');
total_swear_counts = monthly_swear_and_word_totals.('swears');

comment_counts = monthly_swear_and_word_totals.('comments');
total_profane_comment_counts = monthly_swear_and_word_totals.('profane_comments');

% plot total swears over time
figure
hold on

plot(months, total_swear_counts./word_counts);
title('(total swears)/(total words) per month')
xlabel('month')
ylabel('swears/words')
datetick('x', 'yyyy-mm')

% plot profane comments over time
figure
hold on

plot(months, total_profane_comment_counts./comment_counts);
title('(profane comments)/(total comments) per month')
xlabel('month')
ylabel('swears/words')
datetick('x', 'yyyy-mm')

% plot total comments over time
figure
hold on

plot(months, comment_counts);
title('(total comments) per month')
xlabel('month')
ylabel('comment volume')
datetick('x', 'yyyy-mm')


% get counts of each swear for all time
totals = [];

for swear = swears
    swear_string = swear{1};
    monthly_counts = individual_swears_monthly.(swear{1});
    totals = [totals, sum(monthly_counts)];
end

n_desired = 5;
totals = sort(totals,'descend');
top_n_totals = totals(1:n_desired);
next_n_totals = totals(n_desired+1:2*n_desired);

% plot only top n_desired swears over time
figure
hold on

labels = {};
label_count = 1;
for swear = swears
    swear_string = swear{1};
    monthly_counts = individual_swears_monthly.(swear{1});
    if any(sum(monthly_counts)==top_n_totals)
        labels{label_count,1} = swear_string;
        label_count = label_count + 1;
        plot(months, monthly_counts./word_counts, 'linewidth', 3)
    end
end
legend(labels)
title({sprintf('\\makebox[4in][c]{(swear count)/(word count) per month}');
       sprintf('\\makebox[4in][c]{for swears ranked %i to %i}', 1, n_desired)}, 'HorizontalAlignment', 'center')
xlabel('month')
ylabel('swears/words')
datetick('x', 'yyyy-mm')
   

% plot next n_desired swears over time
figure
hold on

labels = {};
label_count = 1;
for swear = swears
    swear_string = swear{1};
    monthly_counts = individual_swears_monthly.(swear{1});
    if any(sum(monthly_counts)==next_n_totals)
        labels{label_count,1} = swear_string;
        label_count = label_count + 1;
        plot(months, monthly_counts./word_counts, 'linewidth', 3)
    end
end
legend(labels)
title({sprintf('\\makebox[4in][c]{(swear count)/(word count) per month}');
       sprintf('\\makebox[4in][c]{for swears ranked %i to %i}', n_desired+1, 2*n_desired)}, 'HorizontalAlignment', 'center')
xlabel('month')
ylabel('swears/words')
datetick('x', 'yyyy-mm')
   

