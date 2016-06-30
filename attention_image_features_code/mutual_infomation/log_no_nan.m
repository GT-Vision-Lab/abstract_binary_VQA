
%log but set nan values to 0
function y=log_no_nan(x)
y=log(x);

ind=isinf(y(:)) | ~isreal(y(:)) | isnan(y(:));

% ind = isinf(y(:));

y(ind)=0; 
% y(ind) = log(eps^2);