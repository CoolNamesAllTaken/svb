%% Input Parameters
a_rnew = 100; % [new accounts per hour] Account growth rate.

d_init = [1 1.5 2 2.5 10]; % [treat credits] Initial deposit for an account.
d_total = 1750; % [treat credits] Total amount of candy purchased.

t_sim = 4 % [hrs] Length of simulation.

i_rate = [1.05 1.1 1.15 1.2]; % [frac] Interest multiplier.
i_step = 1/60; % [hrs] Interest rate compounding interval.

%% What are we optimizing for?
% Inputs:
% - High compounding frequency.
% - Not too much candy.
% Outputs:
% - Large number of open accounts when the bank runs out of treat credits (maximize).
% -


t = [0:i_step:4];

# 3D matrix dimensions: [interest rate, time, initial deposit]
d = zeros(length(i_rate), length(t), length(d_init)); # [treat credits] Required reserves (total deposits).
d(:,1,:) = repmat(d_init, length(i_rate), 1);

a = zeros(size(d)); % [accounts]

for i=2:length(t)
    % Simulation is computed at every interest compounding timestep.
    % TODO: remove proportion of accounts that are closed?
    new_accounts = ones(size(a(:,1,:))) .* (a_rnew * i_step); % add newly created accounts
    a(:,i,:) += new_accounts;
    d(:,i,:) = d(:,i-1,:) .* repmat(i_rate.', 1, 1, length(d_init)); # accrue interest
    d(:,i,:) += new_accounts .* repmat(reshape(d_init, 1, 1, length(d_init)), length(i_rate), 1, 1);

end

% d = (a_rnew .* t) .* (i_rate .^ (t ./ i_step))

figure()
i_rate_labels = {}
for i=1:length(i_rate)
    i_rate_labels{i} = ["i_{rate} = " num2str(i_rate(i))];
end
num_subplots = length(d_init)
subplot(num_subplots, 1, 1);
for i=1:num_subplots
    subplot(num_subplots, 1, i)
    plot(t, d(:,:,i))
    grid on
    ylim([0 d_total])
    title(["Initial Deposit = " num2str(d_init(i))])
    xlabel("Time [hrs]")
    ylabel("Required Reserves [Treat Credits]")
    legend(i_rate_labels, 'location', 'westoutside') % note: this disables zooming!
end

% TODO: make a contour plot
% figure()
% contour(d)
pause
