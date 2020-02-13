from pymedphys.gamma import gamma_shell as gs
import numpy as np
#pymedphys.gamma.gamma_shell(coords_reference, dose_reference, coords_evaluation, dose_evaluation, dose_percent_threshold, distance_mm_threshold)
coords_reference=((1,1),(1,2),(1,3))
dose_reference=[[1,1],[1.1,1.1],[1.2,1.2]]
dose_reference=np.array(dose_reference)
print(dose_reference.shape,"er shape til dose_reference")
print(np.size(coords_reference)/len(coords_reference), len(coords_reference), "er size og len til coords_reference")

coords_evaluation=((1,1),(1,2),(1,3))
dose_evaluation=[[1,1],[1.1,1.2],[1.2,1.3]]

dose_percent_threshold=1
distance_mm_threshold=1
gs(coords_reference, dose_reference, coords_evaluation, dose_evaluation, dose_percent_threshold, distance_mm_threshold)


