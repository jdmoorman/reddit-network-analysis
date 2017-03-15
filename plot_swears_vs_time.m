%% overall swears
clc
close all
clear all

individual_swears_monthly = import_individual_swears_monthly('./output/individual_swears_monthly.csv');
monthly_swear_and_word_totals = import_monthly_swear_and_word_totals('./output/monthly_swear_and_word_totals.csv');

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
xlim([start_month end_month])

% plot profane comments over time
figure
hold on

plot(months, total_profane_comment_counts./comment_counts);
title('(profane comments)/(total comments) per month')
xlabel('month')
ylabel('profane/total')
datetick('x', 'yyyy-mm')
xlim([start_month end_month])

% plot total words over time
figure
hold on

bar(months, word_counts, 1,'FaceColor',[0 .5 .8],'EdgeColor',[0 .5 .8]);
title('(total words) per month')
xlabel('month')
ylabel('word volume')
datetick('x', 'yyyy-mm')
xlim([start_month end_month])

% plot total comments over time
figure
hold on

bar(months, comment_counts, 1,'FaceColor',[0 .5 .8],'EdgeColor',[0 .5 .8]);
title('(total comments) per month')
xlabel('month')
ylabel('comment volume')
datetick('x', 'yyyy-mm')
xlim([start_month end_month])

% plot words per comment over time
figure
hold on

plot(months, word_counts./comment_counts);
title('(total words)/(total comments) per month')
xlabel('month')
ylabel('words/comments')
datetick('x', 'yyyy-mm')
xlim([start_month end_month])


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
legend(labels,'Location','northwest')
title({sprintf('\\makebox[4in][c]{(swear count)/(word count) per month}');
       sprintf('\\makebox[4in][c]{for swears ranked %i to %i}', 1, n_desired)}, 'HorizontalAlignment', 'center')
xlabel('month')
ylabel('swears/words')
datetick('x', 'yyyy-mm')
xlim([start_month end_month])
   
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
legend(labels,'Location','northwest')
title({sprintf('\\makebox[4in][c]{(swear count)/(word count) per month}');
       sprintf('\\makebox[4in][c]{for swears ranked %i to %i}', n_desired+1, 2*n_desired)}, 'HorizontalAlignment', 'center')
xlabel('month')
ylabel('swears/words')
datetick('x', 'yyyy-mm')
xlim([start_month end_month])

%% Swears per Subreddit

comments_per_subreddit = spconvert(load('./output/comments_per_subreddit_sparse.dat'));
profane_comments_per_subreddit = spconvert(load('./output/profane_comments_per_subreddit_sparse.dat'));
swears_per_subreddit = spconvert(load('./output/swears_per_subreddit_sparse.dat'));
words_per_subreddit = spconvert(load('./output/words_per_subreddit_sparse.dat'));

months = import_single_column_csv('./output/months.csv');
subreddits = import_single_column_csv('./output/subreddits.csv');
n_subreddits = size(subreddits,1);
n_months = size(months,1);

start_month = datenum(months{1})
end_month = datenum(months{n_months})

months_linspace = linspace(start_month, end_month, n_months);


% # of subreddits with > 0 comments over time

figure
hold on

for n = 1:6
    subplot(2,3,n)
    n_subreddits_over_time = full(sum((comments_per_subreddit>=10^(n-1)),2));
    plot(months_linspace, n_subreddits_over_time)
    title(sprintf('$\\textgreater$ %i comments',10^(n-1)), 'HorizontalAlignment', 'center')
    xlabel('month')
    ylabel('subreddit count')
    datetick('x', 'yyyy-mm')
    xlim([start_month end_month])
end

figure
hold on

for n = 1:6
    subplot(2,3,n)
    n_subreddits_over_time = full(sum((comments_per_subreddit>=10^(n-1)),2))./full(sum((comments_per_subreddit>=1),2));
    plot(months_linspace, n_subreddits_over_time)
    title(sprintf('$\\textgreater$ %i comments',10^(n-1)), 'HorizontalAlignment', 'center')
    xlabel('month')
    ylabel('ratio')
    datetick('x', 'yyyy-mm')
    xlim([start_month end_month])
end

figure
hold on

n_subreddits_over_time = full(sum((comments_per_subreddit>=1),2));
scatter(months_linspace, n_subreddits_over_time, 150, 'filled')
datetick('x', 'yyyy-mm')
title(sprintf('Reddit begins allowing user submitted subreddits'), 'HorizontalAlignment', 'center')
plot([datenum('2008-01'), datenum('2008-01')], [0, 2000])
xlabel('month')
ylabel('subreddit count')
xlim([start_month end_month])
    
% comment counts per month for top n subreddits in total comment counts

n_desired = 5;
totals = full(sum(comments_per_subreddit, 1));

top_n_totals = sort(totals, 'descend');
top_n_totals = top_n_totals(1:n_desired);
top_n_totals_comments = top_n_totals;

figure
hold on

labels = {};
label_count = 1;
for i = 1:n_subreddits
    if any(totals(i)==top_n_totals)
        labels{label_count,1} = subreddits{i};
        label_count = label_count + 1;
        plot(months_linspace, comments_per_subreddit(:,i), 'linewidth', 3)
    end
end
legend(labels,'Location','northwest')
title({sprintf('\\makebox[4in][c]{(total comments) per month}');
       sprintf('\\makebox[4in][c]{for subreddits ranked %i to %i in comment counts}', 1, n_desired)}, 'HorizontalAlignment', 'center')
xlabel('month')
ylabel('comment volume')
datetick('x', 'yyyy-mm')
xlim([start_month end_month])


% total words for top n subreddits with most total words

n_desired = 5;
totals = full(sum(words_per_subreddit, 1));

top_n_totals = sort(totals, 'descend');
top_n_totals = top_n_totals(1:n_desired);
top_n_totals_words = top_n_totals;

figure
hold on

labels = {};
label_count = 1;
for i = 1:n_subreddits
    if any(totals(i)==top_n_totals)
        labels{label_count,1} = subreddits{i};
        label_count = label_count + 1;
        plot(months_linspace, words_per_subreddit(:,i), 'linewidth', 3)
    end
end
legend(labels,'Location','northwest')
title({sprintf('\\makebox[4in][c]{(word count) per month}');
       sprintf('\\makebox[4in][c]{for subreddits ranked %i to %i in word counts}', 1, n_desired)}, 'HorizontalAlignment', 'center')
xlabel('month')
ylabel('word volume')
datetick('x', 'yyyy-mm')
xlim([start_month end_month])

% words / comments for top n subreddits with most total comments

n_desired = 5;
comments_totals = full(sum(comments_per_subreddit, 1));
words_totals = full(sum(words_per_subreddit, 1));

comments_totals = full(sum(comments_per_subreddit, 1));
words_totals = full(sum(words_per_subreddit, 1));

figure
hold on

labels = {};
label_count = 1;
for i = 1:n_subreddits
    if any(comments_totals(i)==top_n_totals_comments) || any(words_totals(i)==top_n_totals_words)
        labels{label_count,1} = subreddits{i};
        label_count = label_count + 1;
        plot(months_linspace, words_per_subreddit(:,i)./comments_per_subreddit(:,i), 'linewidth', 3)
    end
end
legend(labels,'Location','southwest')
title({sprintf('\\makebox[4in][c]{(word count)/(total comments) per month}');
       sprintf('\\makebox[4in][c]{for subreddits ranked %i to %i in comment count or word count}', 1, n_desired)}, 'HorizontalAlignment', 'center')
xlabel('month')
ylabel('words/comments')
datetick('x', 'yyyy-mm')
xlim([start_month end_month])

% profane comments / total comments for top n subreddits by either words or
% comments

n_desired = 5;
totals = full(sum(comments_per_subreddit, 1));

top_n_totals = sort(totals, 'descend');
top_n_totals = top_n_totals(1:n_desired);

figure
hold on

labels = {};
label_count = 1;
for i = 1:n_subreddits
    if any(totals(i)==top_n_totals)
        labels{label_count,1} = subreddits{i};
        label_count = label_count + 1;
        plot(months_linspace, profane_comments_per_subreddit(:,i)./comments_per_subreddit(:,i), 'linewidth', 3)
    end
end
legend(labels,'Location','northwest')
title({sprintf('\\makebox[4in][c]{(profane comments)/(total comments) per month}');
       sprintf('\\makebox[4in][c]{for subreddits ranked %i to %i in comment counts}', 1, n_desired)}, 'HorizontalAlignment', 'center')
xlabel('month')
ylabel('profane/total')
datetick('x', 'yyyy-mm')
xlim([start_month end_month])

% swears / total words for top n subreddits with most total words

n_desired = 5;
totals = full(sum(words_per_subreddit, 1));

top_n_totals = sort(totals, 'descend');
top_n_totals = top_n_totals(1:n_desired);

figure
hold on

labels = {};
label_count = 1;
for i = 1:n_subreddits
    if any(totals(i)==top_n_totals)
        labels{label_count,1} = subreddits{i};
        label_count = label_count + 1;
        plot(months_linspace, swears_per_subreddit(:,i)./words_per_subreddit(:,i), 'linewidth', 3)
    end
end
legend(labels,'Location','northwest')
title({sprintf('\\makebox[4in][c]{(swear count)/(word count) per month}');
       sprintf('\\makebox[4in][c]{for subreddits ranked %i to %i in word counts}', 1, n_desired)}, 'HorizontalAlignment', 'center')
xlabel('month')
ylabel('swears/words')
datetick('x', 'yyyy-mm')
xlim([start_month end_month])


%%

% What are the most profane subreddits?
swears_per_subreddit = full(sum(spconvert(load('./output/swears_per_subreddit_sparse.dat')),1));
words_per_subreddit = full(sum(spconvert(load('./output/words_per_subreddit_sparse.dat')),1));
subreddits = import_single_column_csv('./output/subreddits.csv')';

n_desired =100;
totals = full(sum(words_per_subreddit, 1));
top_n_totals = sort(totals, 'descend');
top_n_totals = top_n_totals(1:n_desired);
nth_total = top_n_totals(n_desired);
is_in_top_n = totals>=nth_total;

all_ratios = swears_per_subreddit./words_per_subreddit;
top_n_ratios = all_ratios(is_in_top_n);
top_n_subreddits = subreddits(is_in_top_n);
[top_n_ratios, index] = sort(top_n_ratios,'descend');
top_n_subreddits = top_n_subreddits(index);
results = table(top_n_ratios', 'RowNames', top_n_subreddits')

figure
uitable('Data',results{:,:},'ColumnName',{'Swears/Words'},'RowName',results.Properties.RowNames,'Units','Normalized','Position',[0,0,1,1]);

%%

[swears_in_comment,words_in_comment] = import_swear_count_comment_length('./output/swear_count_comment_length.csv');

swears_edges = unique(swears_in_comment);
words_edges = unique(words_in_comment);

regfig = figure;
hold on
xlim([1 100])
logfig = figure;
hold on
xlim([1 100])
set(gca,'YScale','log')
normfig = figure;
hold on
xlim([1 100])

labels = {};
label_count = 1;
for i = 1:6
    labels{label_count,1} = sprintf('comments containing %i swears',i);
    label_count = label_count + 1;
    figure(regfig)
    histogram(words_in_comment(swears_in_comment==i), words_edges)
    figure(logfig)
    histogram(words_in_comment(swears_in_comment==i), words_edges)
    figure(normfig)
    histogram(words_in_comment(swears_in_comment==i), words_edges,'Normalization','probability')
end

figure(regfig)
legend(labels,'Location','northeast')
xlabel('Comment Length')
ylabel('Number of Comments')
title('Histograms of comment length for fixed number of swears')
figure(logfig)
legend(labels,'Location','northeast')
xlabel('Comment Length')
ylabel('Number of Comments')
title('Log scaled histogram of comment length for fixed number of swears')
figure(normfig)
legend(labels,'Location','northeast')
xlabel('Comment Length')
ylabel('Number of Comments')
title('Distribution of comment length for fixed number of swears')










