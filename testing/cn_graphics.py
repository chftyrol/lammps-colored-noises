import matplotlib.pyplot as plt


def plot_list_limited(list, n=100, xlabel="", ylabel="", title="", plot_im_name="plot.png"):
	"Plot (if possible) n first elements from a list and export a png image"

	if n > len(list):
		n = len(list)

	plt.plot(list[:n])
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.ticklabel_format(style="sci", axis="y", scilimits=(0,0))

	plt.savefig(plot_im_name)


def plot_cn(noise_sample, n=100):
	"Plot the graph of a colored noise (n step) and export a png image"

	plot_list_limited(noise_sample, n, "Step", "Volume", "Colored Noise", "cn_plot.png")


def plot_cn_ps(ps_noise_sample, n=100):
	"Plot the graph of the power spectrum of a colored noise\
	(first n frequencies) and export a png image"

	plot_list_limited(ps_noise_sample, n, "Frequency", "Volume", \
	"Colore Noise Power Spectrum", "cn_ps_plot.png")
