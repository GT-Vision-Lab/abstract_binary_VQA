function mi = comp_mi(co_matrix)
%Input co-occurrence matrix and output mutual information

pxy = co_matrix/sum(sum(co_matrix));
px = repmat(sum(pxy,1),size(pxy,1),1);
py = repmat(sum(pxy,2),1,size(pxy,2));

pnn = 1-px-py+pxy;
pyn = px-pxy;
pny = py-pxy;
mi = pxy.*log_no_nan(pxy./px./py) + pnn.*log_no_nan(pnn./(1-px)./(1-py)) + ...
    pyn.*log_no_nan(pyn./px./(1-py)) + pny.*log_no_nan(pny./py./(1-px));