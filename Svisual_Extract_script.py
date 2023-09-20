#################################################
# Sentaurus Visual Console - Python interpreter #
#################################################
# 
#------------------------------
## Define SWB variables
#set Vtgm   x
#set VtiLin x
#set IdLin  x
#set SSlin  x
#set gmLin  x
#set VtiSat x
#set IdSat  x
#set Ioff   x
#set SSsat  x
#set gmSat  x
##Get variables from nodes
Type = '@type@'
vdd = @Vdd@
W = @W@
Lgate = @Lgate@ #um
file_Lin = '@Id_VgLin_filename@'
file_Sat = '@Id_VgSat_filename@'
#-----------------------------------------------------
##swtich
if 'nmos' == Type:
	zz = 1
else:
	zz = -1

Vdd = vdd*zz # for idLin|idSat
##import need package
import svisual as sv
import pandas as pd
import numpy as np
## Import Extraction module
import svisualpylib.extract as ext


## ---------------Condition : Vd=0.05, Id-Vg ----------------------------------------------------------------------
if file_Lin != '0':
	##load file------------------------------------------------------------------
	csv_data = pd.read_csv(file_Lin)
	##get variables from csv data
	np.set_printoptions(precision=4)
	vgs = csv_data.iloc[:, 0].to_numpy()
	ids = csv_data.iloc[:, 1].to_numpy()
	abs_ids = np.abs(ids)
	ids_W= 1e+6*ids/W

	io = 40e-9*W/Lgate  # subthreshold current level [A/um]
	vo = 1e-4
	vgo = vo*zz  # for ss extract

	# ---------------Extract Vtgm\ VtiLin\ SSLin\ IdLin\ gmLin-----------------------------------------------------
	vtgm = ext.extract_vtgm(vgs, abs_ids, name='Vtgm')
	print(f'Vt (Max gm method): {vtgm:.3f} V')

	vti = ext.extract_vti(vgs, ids, io, name="VtiLin")
	print(f'VtiLin: {vti:.3f} V')

	#Idmax = ext.extract_extremum(ids, 'max', name='IdLin')
	idlin = ext.extract_value(vgs,ids_W, x_o= Vdd, name="IdLin", format='.3f')  #uA/um
	print(f'IdiLin: {idlin:.3f} uA')

	gm = ext.extract_gm(vgs, abs_ids, name="gmLin")
	print(f"gmLin: {gm:.3e} S/um")
	sslin = ext.extract_ss(vgs, ids, vgo, name='SSlin')
	print(f"SSlin: {sslin:.3f}")
else:
	pass





'''
# create a poper figure

sv.create_plot(xy=True, name ='1D_plot')

sv.set_plot_prop(show_grid=True,frame_width=2,title_font_size=28)

sv.set_axis_prop(axis='y',\
	title_font_size=28, title_font_color='#000000', title_font_att=['normal'], \
	label_font_family='arial', label_font_size=20, label_font_color='#000000', label_font_att=['normal'])


sv.set_axis_prop(axis='x', \
	title_font_size=28, title_font_color='#000000', title_font_att=['normal'], \
	major_ticks_length=10, major_ticks_width=2, \
	label_font_family='arial', label_font_size=20, label_font_color='#000000', label_font_att=['normal'])

sv.set_legend_prop(label_font_family='arial', label_font_size=24, label_font_color='#000000', label_font_att=['normal'])
'''


#================ Plot id_VgLin curve===========================================
#sv.create_curve(axisX='Vg', axisY='Ids', dataset=dataset_Lin, plot='1D_plot')



# ---------------Condition : Vd=Vdd, Id-Vg ----------------------------------------------------------------------

if file_Sat != '0':
	##load file------------------------------------------------------------------
	csv_data = pd.read_csv(file_Sat)
	
	np.set_printoptions(precision=4)
	vgs = csv_data.iloc[:, 0].to_numpy()
	ids = csv_data.iloc[:, 1].to_numpy()
	abs_ids = np.abs(ids)
	ids_W= 1e+6*ids/W
	
	io = 40e-9*W/Lgate  # subthreshold current level [A/um]
	vo = 1e-2
	vgo = vo*zz # for ss extract
	v_zero = 1e-4*zz # for i_off extract
# ---------------Extract VtiSat\ IdSat\ Ioff\ SSsat\ gmSat------------------------------------------------------
	vtisat = ext.extract_vti(vgs, abs_ids, io, name="VtiSat")
	print(f'VtiSat: {vtisat:.3f} V')

	##Id = ext.extract_extremum(ids, 'max', name="IdSat")
	idsat = ext.extract_value(vgs,ids_W, x_o= Vdd, name="IdSat", format='.3f') #uA/um
	print(f'IdSat: {idsat:.3f} uA')

	abs_ids_W= 1e+12*abs_ids/W
	ioff = ext.extract_ioff(vgs, abs_ids_W, v_o= v_zero, log10=False, name="Ioff", format='.3f')
	print(f"Ioff: {ioff:.3e} pA/um")

	sssat = ext.extract_ss(vgs, ids, vgo, name='SSsat')
	print(f"SSlin: {sssat:.3f}")

	gmsat = ext.extract_gm(vgs, abs_ids, name="gmSat")
	print(f"Max gm: {gmsat:.3e} S/um")
else:
	pass

#
#sv.create_curve(axisX='Vg', axisY=IDS, dataset= dataset_Sat, plot='1D_plot')