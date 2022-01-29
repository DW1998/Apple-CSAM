import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

robustness_dir = "D:/Apple-CSAM-Files/Plots_Robustness_New/"
y_robustness_h = "Unveränderte Hashwerte"
y_robustness_e = "Durchschnittliche Differenz"
collision_dir = "D:/Apple-CSAM-Files/Plots_Collision_New/"
y_collision_d = "Durchschnittliche Differenz bei i = 1.000"
y_collision_c = "Kollisionen bei i = 1.000"


def func_percent(x, pos):
    s = str(round(x, 2))
    ind = s.index('.')
    return s[:ind] + ',' + s[ind + 1:] + '%'


format_percent = mtick.FuncFormatter(func_percent)


def func(x, pos):
    s = str(round(x, 2))
    ind = s.index('.')
    return s[:ind] + ',' + s[ind + 1:]


format_no_percent = mtick.FuncFormatter(func)


def plot_robustness(pdf_name, x_label, x_data, y_data_h, y_data_e, invert, percent_x, comma):
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data_h, "-x")
    plt_robustness_h(ax, x_label, pdf_name, invert, percent_x, comma)
    plt.close(fig)
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data_e, "-x")
    plt_robustness_e(ax, x_label, pdf_name, invert, percent_x, comma)
    plt.close(fig)


def plt_robustness_h(ax, x_label, name, invert, percent_x, comma):
    plt.xlabel(x_label)
    if invert:
        ax.invert_xaxis()
    if percent_x:
        if comma:
            ax.xaxis.set_major_formatter(format_percent)
        else:
            ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    else:
        if comma:
            ax.xaxis.set_major_formatter(format_no_percent)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.ylabel(y_robustness_h)
    plt.grid(True)
    plt.rcdefaults()
    plt.savefig(f"{robustness_dir}{name}.pdf", format='pdf')


def plt_robustness_e(ax, x_label, name, invert, percent_x, comma):
    plt.xlabel(x_label)
    if invert:
        ax.invert_xaxis()
    if percent_x:
        if comma:
            ax.xaxis.set_major_formatter(format_percent)
        else:
            ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    else:
        if comma:
            ax.xaxis.set_major_formatter(format_no_percent)
    plt.ylabel(y_robustness_e)
    plt.grid(True)
    plt.rcdefaults()
    plt.savefig(f"{robustness_dir}{name}_Error.pdf", format='pdf')


def plots_robustness():
    x_resolution = [i * 5 for i in range(0, 21)]
    y_resolution_h = [1, 8, 36, 48, 60, 65, 73, 67, 80, 76, 77, 80, 82, 88, 83, 88, 93, 98, 96, 96, 98]
    y_resolution_e = [6.89, 3.71, 1.24, 0.85, 0.53, 0.44, 0.35, 0.37, 0.23, 0.28, 0.27, 0.23, 0.21, 0.13, 0.18, 0.12, 0.07, 0.02, 0.04, 0.04, 0.02]
    plot_robustness("Resolution", "Auflösungsqualität", x_resolution, y_resolution_h, y_resolution_e, True, True, False)
    x_resize = [i * 5 for i in range(1, 21)]
    y_resize_h = [4, 42, 62, 73, 79, 85, 89, 93, 93, 96, 92, 96, 97, 96, 97, 96, 97, 98, 96, 100]
    y_resize_e = [4.79, 1.16, 0.56, 0.36, 0.24, 0.16, 0.12, 0.08, 0.08, 0.04, 0.08, 0.04, 0.03, 0.04, 0.03, 0.04, 0.03, 0.02, 0.04, 0.0]
    plot_robustness("Resize", "Skalierungsfaktor", x_resize, y_resize_h, y_resize_e, True, True, False)
    x_crop = [i / 4 for i in range(20, -1, -1)]
    y_crop_h = [0, 1, 1, 1, 2, 2, 2, 3, 2, 3, 5, 5, 7, 11, 14, 20, 32, 41, 48, 75, 100]
    y_crop_e = [5.97, 5.64, 5.46, 5.21, 4.91, 4.69, 4.39, 4.02, 3.77, 3.54, 3.19, 2.83, 2.54, 2.26, 1.96, 1.69, 1.34, 1.1, 0.87, 0.34, 0.0]
    plot_robustness("Crop", "Zuschneidungsmenge", x_crop, y_crop_h, y_crop_e, False, True, True)
    x_rotation = [i / 10 for i in range(-10, 11, 1)]
    y_rotation_h = [0, 0, 1, 1, 1, 1, 1, 1, 1, 7, 100, 3, 0, 1, 1, 1, 1, 0, 0, 0, 0]
    y_rotation_e = [6.08, 6.06, 6.02, 5.93, 5.85, 5.64, 5.46, 5.19, 4.88, 3.85, 0, 3.97, 5.01, 5.22, 5.42, 5.54, 5.71, 5.68, 5.77, 5.81, 5.88]
    plot_robustness("Rotation", "Rotationswinkel", x_rotation, y_rotation_h, y_rotation_e, False, False, True)
    x_logo = [i * 2.5 for i in range(0, 21)]
    y_logo_h = [100, 81, 65, 57, 46, 33, 24, 18, 13, 11, 12, 8, 4, 4, 2, 3, 1, 0, 0, 0, 0]
    y_logo_e = [0.0, 0.23, 0.64, 0.94, 1.26, 1.75, 2.3, 2.94, 3.47, 4.06, 4.44, 5.09, 5.93, 6.58, 7.52, 8.51, 9.65, 10.88, 12.04, 13.23, 14.78]
    plot_robustness("Logo", "Wasserzeichengröße", x_logo, y_logo_h, y_logo_e, False, True, False)
    x_contrast = [i * 10 for i in range(0, 21)]
    y_contrast_h = [0, 35, 60, 75, 83, 82, 84, 87, 91, 90, 100, 34, 12, 4, 1, 0, 0, 0, 0, 0, 0]
    y_contrast_e = [47.0, 1.74, 0.68, 0.33, 0.22, 0.21, 0.17, 0.16, 0.1, 0.11, 0.0, 1.83, 4.22, 7.03, 9.72, 12.26, 14.48, 16.58, 18.4, 20.23, 21.86]
    plot_robustness("Contrast", "Kontrast", x_contrast, y_contrast_h, y_contrast_e, False, True, False)
    x_color = [i * 10 for i in range(0, 41)]
    y_color_h = [41, 46, 47, 54, 61, 68, 78, 80, 81, 84, 100, 79, 79, 73, 65, 62, 55, 49, 44, 42, 40, 39, 35, 31, 25, 21, 23, 21, 18, 17, 17, 15, 13, 12, 11, 9, 8, 8, 7, 7, 5]
    y_color_e = [1.02, 0.9, 0.81, 0.64, 0.52, 0.39, 0.27, 0.24, 0.21, 0.17, 0.0, 0.3, 0.37, 0.51, 0.66, 0.77, 0.99, 1.21, 1.42, 1.59, 1.71, 1.86, 2.07, 2.28, 2.6, 2.89, 3.14, 3.36, 3.63, 4.0, 4.35, 4.63, 4.92, 5.33, 5.7, 5.99, 6.28, 6.64, 6.82, 7.22, 7.54]
    plot_robustness("Color", "Farbintensität", x_color, y_color_h, y_color_e, False, True, False)
    x_brightness = [i * 10 for i in range(0, 21)]
    y_brightness_h = [0, 3, 10, 39, 59, 66, 80, 90, 89, 89, 100, 42, 11, 4, 3, 0, 0, 0, 0, 0, 0]
    y_brightness_e = [46.83, 4.85, 2.52, 1.1, 0.57, 0.45, 0.26, 0.12, 0.13, 0.13, 0.0, 2.44, 6.56, 10.9, 15.54, 19.98, 23.38, 26.01, 28.5, 30.49, 32.38]
    plot_robustness("Brightness", "Helligkeit", x_brightness, y_brightness_h, y_brightness_e, False, True, False)


def plot_collision(pdf_name, x_label, x_data, y_data_h, y_data_e, comma):
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data_h, "-x")
    plt_collision_d(ax, x_label, pdf_name, comma)
    plt.close(fig)
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data_e, "-x")
    plt_collision_c(ax, x_label, pdf_name, comma)
    plt.close(fig)


def plt_collision_d(ax, x_label, name, comma):
    if comma:
        ax.xaxis.set_major_formatter(format_no_percent)
    plt.xlabel(x_label)
    ax.yaxis.set_major_formatter(format_no_percent)
    plt.ylabel(y_collision_d)
    plt.grid(True)
    plt.savefig(f"{collision_dir}{name}_d.pdf", format='pdf')


def plt_collision_c(ax, x_label, name, comma):
    if comma:
        ax.xaxis.set_major_formatter(format_no_percent)
    plt.xlabel(x_label)
    ax.yaxis.set_major_formatter(format_percent)
    plt.ylabel(y_collision_c)
    plt.grid(True)
    plt.savefig(f"{collision_dir}{name}_c.pdf", format='pdf')


def plots_collision():
    x_k = [l for l in range(5, 21)]
    y_k_d = [4.54, 4.78, 3.84, 3.54, 3.5, 3.42, 3.48, 3.18, 3.48, 3.46, 3.0, 3.2, 3.22, 3.34, 3.52, 3.62]
    y_k_c = [l * 2 for l in [13, 13, 16, 19, 22, 22, 22, 26, 27, 25, 27, 30, 31, 29, 27, 27]]
    plot_collision("k", "k", x_k, y_k_d, y_k_c, False)
    x_clip_r = [l / 20 for l in range(10)]
    y_clip_r_d = [3.6, 3.42, 3.42, 3.52, 3.52, 3.74, 5.22, 7.06, 9.32, 20.68]
    y_clip_r_c = [l * 2 for l in [20, 22, 22, 25, 28, 28, 27, 18, 13, 0]]
    plot_collision("clip_r", "c", x_clip_r, y_clip_r_d, y_clip_r_c, True)
    x_lr = [l / 2 for l in range(1, 21)]
    y_lr_d = [6.12, 4.32, 3.66, 3.42, 3.28, 3.24, 3.0, 2.94, 2.98, 2.98, 3.0, 2.82, 2.72, 2.9, 2.8, 2.9, 2.68, 2.82, 2.82, 3.0]
    y_lr_c = [l * 2 for l in [9, 16, 21, 22, 23, 23, 27, 29, 26, 26, 26, 30, 27, 26, 28, 26, 29, 28, 29, 26]]
    plot_collision("lr", "α", x_lr, y_lr_d, y_lr_c, False)
    x_blur = [l / 10 for l in range(11)]
    y_blur_d = [3.42, 3.54, 3.56, 4.04, 5.24, 6.76, 7.42, 7.96, 8.74, 9.32, 10.5]
    y_blur_c = [l * 2 for l in [22, 22, 22, 16, 11, 8, 6, 6, 6, 6, 4]]
    plot_collision("blur", "σ", x_blur, y_blur_d, y_blur_c, True)
    y_blur_optimized_c = [l * 2 for l in [38, 38, 37, 34, 32, 31, 27, 27, 26, 23, 20]]
    fig, ax = plt.subplots()
    ax.plot(x_blur, y_blur_c, "-x", label="Default")
    ax.plot(x_blur, y_blur_optimized_c, "-x", label="Optimiert")
    ax.xaxis.set_major_formatter(format_no_percent)
    plt.xlabel("σ")
    plt.ylabel(y_collision_c)
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{collision_dir}Comparison_Blur_c.pdf", format='pdf')
    plt.close(fig)
    x_1000 = [1]
    for l in range(1, 41):
        x_1000.append(l * 25)
    y_1000_default = [47.88, 28.96, 20.3, 15.4, 12.6, 10.74, 9.34, 8.56, 8.0, 7.42, 7.0, 6.62, 6.34, 6.06, 5.8, 5.6,
                      5.32, 5.12, 4.94, 4.82, 4.7, 4.44, 4.26, 4.16, 4.12, 4.06, 3.96, 3.94, 3.88, 3.88, 3.84, 3.76,
                      3.74, 3.68, 3.64, 3.56, 3.52, 3.5, 3.44, 3.42, 3.42]
    y_1000_optimized = [47.88, 16.2, 10.26, 7.64, 6.22, 5.46, 4.86, 4.48, 4.18, 3.96, 3.78, 3.62, 3.38, 3.22, 3.16,
                        3.1, 3.06, 3.04, 3.0, 2.98, 2.96, 2.94, 2.9, 2.7, 2.66, 2.64, 2.6, 2.58, 2.58, 2.58, 2.56,
                        2.52, 2.42, 2.42, 2.4, 2.38, 2.38, 2.36, 2.36, 2.34, 2.3]
    fig, ax = plt.subplots()
    ax.plot(x_1000, y_1000_default, "-x", label="Default")
    ax.plot(x_1000, y_1000_optimized, "-x", label="Optimiert")
    plt.xlabel("Iteration")
    plt.ylabel("Durchschnittliche Differenz")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{collision_dir}Comparison.pdf", format='pdf')
    plt.close(fig)
    y_1000_default_blur1 = [47.88, 35.26, 29.72, 26.24, 22.96, 21.12, 19.74, 18.4, 17.42, 16.82, 16.08, 15.56, 15.16,
                            14.82, 14.34, 13.98, 13.6, 13.38, 13.16, 13.08, 12.98, 12.76, 12.66, 12.38, 12.22, 12.14,
                            11.9, 11.66, 11.38, 11.3, 11.22, 11.2, 11.12, 10.98, 10.86, 10.74, 10.7, 10.62, 10.56,
                            10.52, 10.5]
    y_1000_optimized_blur1 = [47.88, 20.42, 14.36, 11.8, 10.44, 9.86, 9.1, 8.48, 8.0, 7.52, 7.3, 7.02, 6.68, 6.52,
                              6.38, 6.08, 5.82, 5.66, 5.48, 5.36, 5.32, 5.1, 4.98, 4.94, 4.8, 4.64, 4.46, 4.42,
                              4.34, 4.34, 4.32, 4.22, 4.1, 4.06, 4.04, 3.88, 3.86, 3.76, 3.7, 3.7, 3.7]
    fig, ax = plt.subplots()
    ax.plot(x_1000, y_1000_default_blur1, "-x", label="Default mit σ = 1,0")
    ax.plot(x_1000, y_1000_optimized_blur1, "-x", label="Optimiert mit σ = 1,0")
    plt.xlabel("Iteration")
    plt.ylabel("Durchschnittliche Differenz")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{collision_dir}Comparison_Blur1.0.pdf", format='pdf')
    plt.close(fig)


def main():
    plots_robustness()
    plots_collision()


if __name__ == '__main__':
    main()
