import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as patches

def info_boxplot(ax, data, median_linestyle='solid', median_linewidth=1, median_color='black',
                 upper_whisker_linestyle='solid', upper_whisker_linewidth=1, upper_whisker_color='black',
                 lower_whisker_linestyle='solid', lower_whisker_linewidth=1, lower_whisker_color='black',
                 outliers_color='gray', outliers_linecolor='black',
                 box_facecolor='white', box_linestyle='solid', box_linewidth=1, box_linecolor='black',
                 multiplebox=True, show_outliers=True):
    count = 0

    if type(data[0]) != list:
        print("Warning：Please input the data with format: lists in a list   Example: [[1,2,3,4], [5,6,7,8], [9,10,11,12]] ")
        data = [data]
    #Find the maximum and minimum values ​​in all data to determine the scale range of the axis

    z_max_list = []
    z_min_list = []
    x_range_list = []
    y_range_list = []
    for z in data:
        z_max = max(z)
        z_max_list.append(z_max)
        z_min =min(z)
        z_min_list.append(z_min)
    max_range = max(z_max_list)
    min_range = min(z_min_list)



    for z in data:
        z.sort()
        #print(z)
        # Determine the position of each Q line in the data set
        n = len(z)
        d = float(0)
        Q_position = []
        for i in np.arange(11):
            q = (n + 1) * (0.25 + d)
            Q_position.append(q)
            d += 0.05
        # print(Q_position)


        # Determine the value of the Q line
        result = []
        for i in Q_position:
            if math.modf(i)[0] == 0.0:
                Q_value = z[int(i) - 1]
                result.append(Q_value)
            else:
                x = math.modf(i)
                Q_value = (x[0] * z[int(x[1])]) + (1 - x[0]) * z[int(x[1] - 1)]
                result.append(Q_value)
        # print(result)

        # Calculate upper and lower bounds and outliers
        Q1 = result[0]
        Q3 = result[10]
        IQR = Q3 - Q1
        upper_fence = Q3 + 1.5 * IQR
        low_fence = Q1 - 1.5 * IQR
        result.sort()

        low_outlier = []
        upper_outlier = []
        for i in z:
            if i < low_fence:
                low_outlier.append(i)
            if i > upper_fence:
                upper_outlier.append(i)
        if len(low_outlier) == 0:
            result.append(z[0])
        else:
            result.append(low_fence)
        if len(upper_outlier) == 0:
            result.append(z[-1])
        else:
            result.append(upper_fence)

        # Determine the scale range of the X coordinate axis according to the number of box plots
        result.sort()
        x_range = max(result)
        x_range_list.append(x_range)
        real_x_range = max(x_range_list)
        y_range = min(result)
        y_range_list.append(y_range)
        real_y_range = max(y_range_list)
        if show_outliers == True:
            if y_range < 0:
                ax.set_ylim((1.2 * min_range, 1.2 * max_range))
            else:
                ax.set_ylim((0, 1.2 * max_range))
        else:
            if y_range < 0:
                ax.set_ylim((1.2 * real_y_range, 1.2 * real_x_range))
            else:
                ax.set_ylim((0, 1.2 * real_x_range))
        ax.set_xlim(0, 40 * len(data))

        # Use rectangles to generate boxes and paint them
        x = 14 + 40 * count
        ax.add_patch(
            patches.Rectangle((x, result[1]), 12, (result[11] - result[1]), facecolor=box_facecolor, edgecolor='white'))

        # Draw the whiskers and the line between the box and the whiskers
        a = 1
        for i in result:
            x = 14 + 40 * count
            y = 26 + 40 * count
            if a == 1:
                x = 17 + 40 * count
                y = 23 + 40 * count
                line = mlines.Line2D([x, y], [i, i], color=lower_whisker_color, linestyle=lower_whisker_linestyle,
                                     linewidth=lower_whisker_linewidth)
                ax.add_line(line)
            elif a == len(result):
                x = 17 + 40 * count
                y = 23 + 40 * count
                line = mlines.Line2D([x, y], [i, i], color=upper_whisker_color, linestyle=upper_whisker_linestyle,
                                     linewidth=upper_whisker_linewidth)
                ax.add_line(line)
            elif a == 7:
                line = mlines.Line2D([x, y], [i, i], color=median_color, linestyle=median_linestyle,
                                     linewidth=median_linewidth)
                ax.add_line(line)
            elif a == 2 or a == 12:
                line = mlines.Line2D([x, y], [i, i], color=box_linecolor, linestyle=box_linestyle,
                                     linewidth=box_linewidth)
                ax.add_line(line)
            else:
                if multiplebox == True:
                    line = mlines.Line2D([x, y], [i, i],color = 'black')
                    ax.add_line(line)
            a += 1

        x = 20 + 40 * count
        y = 14 + 40 * count
        f = 26 + 40 * count
        line_ver1 = mlines.Line2D([x, x], [result[0], result[1]], color=box_linecolor, linestyle=box_linestyle,
                                  linewidth=box_linewidth)
        ax.add_line(line_ver1)
        line_ver2 = mlines.Line2D([x, x], [result[-1], result[11]], color=box_linecolor, linestyle=box_linestyle,
                                  linewidth=box_linewidth)
        ax.add_line(line_ver2)
        line_ver3 = mlines.Line2D([y, y], [result[11], result[1]], color=box_linecolor, linestyle=box_linestyle,
                                  linewidth=box_linewidth)
        ax.add_line(line_ver3)
        line_ver4 = mlines.Line2D([f, f], [result[11], result[1]], color=box_linecolor, linestyle=box_linestyle,
                                  linewidth=box_linewidth)
        ax.add_line(line_ver4)

        # Draw outliers
        if show_outliers == True:
            for i in upper_outlier:
                x = 20 + 40 * count
                height = max_range/100
                ax.add_patch(patches.Ellipse((x, i), 2, height, facecolor=outliers_color, edgecolor=outliers_linecolor))

            for i in low_outlier:
                x = 20 + 40 * count
                height = max_range/100
                ax.add_patch(patches.Ellipse((x, i), 2, height, facecolor=outliers_color, edgecolor=outliers_linecolor))
        count += 1

    plt.xticks([])
    plt.show()


def histobox_plot(ax, data, median_linestyle='solid', median_linewidth=1, median_color='black',
             upper_whisker_linestyle='solid', upper_whisker_linewidth=1, upper_whisker_color='black',
             lower_whisker_linestyle='solid', lower_whisker_linewidth=1, lower_whisker_color='black',
             outliers_color='gray', outliers_linecolor='black',
             box_facecolor='white', box_linestyle='solid', box_linewidth=1, box_linecolor='black',
             histo_facecolor='gray', histo_linecolor='black', show_outliers = True):


    count = 0
    if type(data[0]) != list:
        print("Warning：Please input the data with format: lists in a list   Example: [[1,2,3,4], [5,6,7,8], [9,10,11,12]] ")
        data = [data]

    #Find the maximum and minimum values ​​in all data to determine the scale range of the axis
    z_max_list = []
    z_min_list = []
    x_range_list = []
    y_range_list = []
    for z in data:
        z_max = max(z)
        z_max_list.append(z_max)
        z_min =min(z)
        z_min_list.append(z_min)
    max_range = max(z_max_list)
    min_range = min(z_min_list)

    for z in data:
        z.sort()
        #print(z)

        # Determine the position of each Q line in the data set
        n = len(z)
        d = float(0)
        Q_position = []
        for i in np.arange(11):
            q = (n + 1) * (0.25 + d)
            Q_position.append(q)
            d += 0.05
        #print(Q_position)

        #  Determine the value of the Q line
        result = []
        for i in Q_position:
            if math.modf(i)[0] == 0.0:
                Q_value = z[int(i) - 1]
                result.append(Q_value)
            else:
                x = math.modf(i)
                Q_value = (x[0] * z[int(x[1])]) + (1 - x[0]) * z[int(x[1] - 1)]
                result.append(Q_value)
        #print(result)

        Q1 = result[0]
        Q3 = result[10]
        IQR = Q3 - Q1
        upper_fence = Q3 + 1.5 * IQR
        low_fence = Q1 - 1.5 * IQR
        result.sort()

        low_outlier = []
        upper_outlier = []
        for i in z:
            if i < low_fence:
                low_outlier.append(i)
            if i > upper_fence:
                upper_outlier.append(i)
        if len(low_outlier) == 0:
            result.append(z[0])
        else:
            result.append(low_fence)
        if len(upper_outlier) == 0:
            result.append(z[-1])
        else:
            result.append(upper_fence)

        # Determine the scale range of the X coordinate axis according to the number of box plots
        result.sort()
        x_range = max(result)
        x_range_list.append(x_range)
        real_x_range = max(x_range_list)
        y_range = min(result)
        y_range_list.append(y_range)
        real_y_range = max(y_range_list)
        if show_outliers == True:
            if y_range < 0:
                ax.set_ylim((1.2 * min_range, 1.2 * max_range))
            else:
                ax.set_ylim((0, 1.2 * max_range))
        else:
            if y_range < 0:
                ax.set_ylim((1.2 * real_y_range, 1.2 * real_x_range))
            else:
                ax.set_ylim((0, 1.2 * real_x_range))
        ax.set_xlim(0, 40 * len(data))

        #Count the amount of data in a histo and record it
        step = max(result)/10
        step_ini = 0
        step_list = []
        for i in np.arange(11):
            step_list.append(step_ini)
            step_ini = step_ini + step
        #print(step_list)
        new_z = []
        for i in z:
            if low_fence < i < upper_fence:
                new_z.append(i)
        #print(new_z)
        step_count = 0
        new_z_count = 0
        histo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in np.arange(10000):
            if step_count == 10 or new_z_count == len(new_z):
                break
            if step_list[step_count] <= new_z[new_z_count] < step_list[step_count + 1]:
                histo[step_count] += 1
                #print(histo)
                new_z_count += 1
                #print(new_z_count)
            else:
                step_count += 1
                #print(step_count)
        for i in np.arange(len(histo)):
            histo[i] = histo[i] / len(new_z)
        #print(histo)
        for i in np.arange(len(histo)):
            x = 20 + 40 * count
            y = result[0] + step * i
            judge = y + step
            if judge > result[-1]:
                step = result[-1] - y
            ax.add_patch(patches.Rectangle((x, y), (40 * histo[i]), step,
                                           facecolor=histo_facecolor, edgecolor=histo_linecolor))

    # Use rectangles to generate boxes and paint them
        x = 14 + 40 * count
        ax.add_patch(patches.Rectangle((x, result[1]), 6, (result[11] - result[1]), facecolor=box_facecolor, edgecolor='white'))
    # Draw the whiskers and the line between the box and the whiskers
        a = 1
        for i in result:
            x = 14 + 40 * count
            y = 20 + 40 * count
            if a == 1 or a == len(result):
                x = 17 + 40 * count
                y = 23 + 40 * count
                line = mlines.Line2D([x, y], [i, i], color=lower_whisker_color, linestyle=lower_whisker_linestyle, linewidth=lower_whisker_linewidth)
                ax.add_line(line)
            elif a == len(result):
                x = 17 + 40 * count
                y = 23 + 40 * count
                line = mlines.Line2D([x, y], [i, i], color=upper_whisker_color, linestyle=upper_whisker_linestyle,
                                     linewidth=upper_whisker_linewidth)
            elif a == 7:
                line = mlines.Line2D([x, y], [i, i], color=median_color, linestyle=median_linestyle,
                                     linewidth=median_linewidth)
                ax.add_line(line)
            elif a == 2 or a == 12:
                line = mlines.Line2D([x, y], [i, i], color=box_linecolor, linestyle=box_linestyle,
                                     linewidth=box_linewidth)
                ax.add_line(line)
            a += 1
        x = 20 + 40 * count
        y = 14 + 40 * count
        f = 20 + 40 * count
        line_ver1 = mlines.Line2D([x, x], [result[0], result[1]], color=box_linecolor, linestyle=box_linestyle,
                                     linewidth=box_linewidth)
        ax.add_line(line_ver1)
        line_ver2 = mlines.Line2D([x, x], [result[-1], result[11]], color=box_linecolor, linestyle=box_linestyle,
                                     linewidth=box_linewidth)
        ax.add_line(line_ver2)
        line_ver3 = mlines.Line2D([y, y], [result[11], result[1]], color=box_linecolor, linestyle=box_linestyle,
                                     linewidth=box_linewidth)
        ax.add_line(line_ver3)
        line_ver4 = mlines.Line2D([f, f], [result[11], result[1]], color=box_linecolor, linestyle=box_linestyle,
                                     linewidth=box_linewidth)
        ax.add_line(line_ver4)

        # Draw Outliers
        if show_outliers == True:
            for i in upper_outlier:
                x = 20 + 40 * count
                height = max_range/100
                ax.add_patch(patches.Ellipse((x, i), 2, height, facecolor=outliers_color, edgecolor=outliers_linecolor))

            for i in low_outlier:
                x = 20 + 40 * count
                height = max_range/100
                ax.add_patch(patches.Ellipse((x, i), 2, height, facecolor=outliers_color, edgecolor=outliers_linecolor))
        count += 1

    plt.xticks([])
    plt.show()


def creative_boxplot(ax, data, median_linestyle='solid', median_linewidth=1, median_color='black',
                     upper_whisker_linestyle='solid', upper_whisker_linewidth=1, upper_whisker_color='black',
                     lower_whisker_linestyle='solid', lower_whisker_linewidth=1, lower_whisker_color='black',
                     outliers_color='gray', outliers_linecolor='black',
                     box_facecolor='white', box_linestyle='solid', box_linewidth=1, box_linecolor='black',
                     gradient_gray=True, gradient_color=(0.1, 0.7, 0.7),
                     multiplebox=False, show_outliers=True):
    count = 0
    if type(data[0]) != list:
        print("Warning：Please input the data with format: lists in a list   Example: [[1,2,3,4], [5,6,7,8], [9,10,11,12]] ")
        data = [data]
    # Find the maximum and minimum values ​​in all data to determine the scale range of the axis
    z_max_list = []
    z_min_list = []
    x_range_list = []
    y_range_list = []
    for z in data:
        z_max = max(z)
        z_max_list.append(z_max)
        z_min = min(z)
        z_min_list.append(z_min)
    max_range = max(z_max_list)
    min_range = min(z_min_list)

    for z in data:
        z.sort()
        # print(z)

        # Determine the position of each Q line in the data set
        n = len(z)
        d = float(0)
        Q_position = []
        for i in np.arange(11):
            q = (n + 1) * (0.25 + d)
            Q_position.append(q)
            d += 0.05
        # print(Q_position)

        # Determine the value of each Q line
        result = []
        for i in Q_position:
            if math.modf(i)[0] == 0.0:
                Q_value = z[int(i) - 1]
                result.append(Q_value)
            else:
                x = math.modf(i)
                Q_value = (x[0] * z[int(x[1])]) + (1 - x[0]) * z[int(x[1] - 1)]
                result.append(Q_value)
        # print(result)

        # Calculate upper and lower bounds and outliers
        Q1 = result[0]
        Q3 = result[10]
        IQR = Q3 - Q1
        upper_fence = Q3 + 1.5 * IQR
        low_fence = Q1 - 1.5 * IQR
        result.sort()

        low_outlier = []
        upper_outlier = []
        for i in z:
            if i < low_fence:
                low_outlier.append(i)
            if i > upper_fence:
                upper_outlier.append(i)
        if len(low_outlier) == 0:
            result.append(z[0])
        else:
            result.append(low_fence)
        if len(upper_outlier) == 0:
            result.append(z[-1])
        else:
            result.append(upper_fence)

        # Determine the scale range of the X coordinate axis according to the number of box plots
        result.sort()
        x_range = max(result)
        x_range_list.append(x_range)
        real_x_range = max(x_range_list)
        y_range = min(result)
        y_range_list.append(y_range)
        real_y_range = max(y_range_list)
        if show_outliers == True:
            if y_range < 0:
                ax.set_ylim((1.2 * min_range, 1.2 * max_range))
            else:
                ax.set_ylim((0, 1.2 * max_range))
        else:
            if y_range < 0:
                ax.set_ylim((1.2 * real_y_range, 1.2 * real_x_range))
            else:
                ax.set_ylim((0, 1.2 * real_x_range))
        ax.set_xlim(0, 40 * len(data))

        # Judge if the user want to use the creative idea
        if gradient_gray == False:
            x = 14 + 40 * count
            ax.add_patch(patches.Rectangle((x, result[1]), 12, (result[11] - result[1]), facecolor=box_facecolor,
                                           edgecolor='white'))

        if gradient_gray == True:
            step = (result[11] - result[1]) / 20
            step_ini = 0
            step_list = []
            for i in np.arange(21):
                step_list.append(step_ini)
                step_ini = step_ini + step
            # print(step_list)
            new_z = []
            for i in z:
                if low_fence < i < upper_fence:
                    new_z.append(i)
            # print(new_z)
            step_count = 0
            new_z_count = 0

            histo = [0 for makezero in range(20)]
            #print(histo)

            for i in np.arange(10000):
                if step_count == 20 or new_z_count == len(new_z):
                    break
                if step_list[step_count] <= new_z[new_z_count] < step_list[step_count + 1]:
                    histo[step_count] += 1
                    # print(histo)
                    new_z_count += 1
                    # print(new_z_count)
                else:
                    step_count += 1
                    # print(step_count)
            # print(histo)
            for i in np.arange(len(histo)):
                histo[i] = (histo[i] / len(new_z)) * 100
            colorlist = []
            for i in histo:
                temp1 = 0.1 * i
                temp2 = float(temp1)
                if temp2 >= 1:
                    temp2 = 1
                colorlist.append(temp2)
            # print(colorlist)
            gradientcolor_list = []
            for j in gradient_color:
                gradientcolor_list.append(j)
            # print(gradientcolor_list)
            for i in np.arange(len(histo)):
                x = 14 + 40 * count
                z = result[1] + step * i
                ax.add_patch(patches.Rectangle((x, z), 12, step, edgecolor='white', linewidth=0, facecolor=(
                gradientcolor_list[0], gradientcolor_list[1], gradientcolor_list[2], colorlist[i])))

        a = 1
        for i in result:
            x = 14 + 40 * count
            y = 26 + 40 * count
            if a == 1:
                x = 17 + 40 * count
                y = 23 + 40 * count
                line = mlines.Line2D([x, y], [i, i], color=lower_whisker_color, linestyle=lower_whisker_linestyle,
                                     linewidth=lower_whisker_linewidth)
                ax.add_line(line)
            elif a == len(result):
                x = 17 + 40 * count
                y = 23 + 40 * count
                line = mlines.Line2D([x, y], [i, i], color=upper_whisker_color, linestyle=upper_whisker_linestyle,
                                     linewidth=upper_whisker_linewidth)
                ax.add_line(line)
            elif a == 7:
                line = mlines.Line2D([x, y], [i, i], color=median_color, linestyle=median_linestyle,
                                     linewidth=median_linewidth)
                ax.add_line(line)
            elif a == 2 or a == 12:
                line = mlines.Line2D([x, y], [i, i], color=box_linecolor, linestyle=box_linestyle,
                                     linewidth=box_linewidth)
                ax.add_line(line)
            else:
                if multiplebox == True:
                    line = mlines.Line2D([x, y], [i, i])
                    ax.add_line(line)
            a += 1

        x = 20 + 40 * count
        y = 14 + 40 * count
        f = 26 + 40 * count
        line_ver1 = mlines.Line2D([x, x], [result[0], result[1]], color=box_linecolor, linestyle=box_linestyle,
                                  linewidth=box_linewidth)
        ax.add_line(line_ver1)
        line_ver2 = mlines.Line2D([x, x], [result[-1], result[11]], color=box_linecolor, linestyle=box_linestyle,
                                  linewidth=box_linewidth)
        ax.add_line(line_ver2)
        line_ver3 = mlines.Line2D([y, y], [result[11], result[1]], color=box_linecolor, linestyle=box_linestyle,
                                  linewidth=box_linewidth)
        ax.add_line(line_ver3)
        line_ver4 = mlines.Line2D([f, f], [result[11], result[1]], color=box_linecolor, linestyle=box_linestyle,
                                  linewidth=box_linewidth)
        ax.add_line(line_ver4)

        if show_outliers == True:
            for i in upper_outlier:
                x = 20 + 40 * count
                height = max_range / 100
                ax.add_patch(patches.Ellipse((x, i), 2, height, facecolor=outliers_color, edgecolor=outliers_linecolor))

            for i in low_outlier:
                x = 20 + 40 * count
                height = max_range / 100
                ax.add_patch(patches.Ellipse((x, i), 2, height, facecolor=outliers_color, edgecolor=outliers_linecolor))
        count += 1

    plt.xticks([])
    plt.show()



