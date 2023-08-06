from matplotlib.widgets import Slider, Button
import matplotlib.pyplot as plt
import sympy as sp
from numpy import vectorize


def slider(
    expr,
    x,
    params,
    xdata,
    lambdify_kws=None,
    plot_kws=None,
    use_latex=False,
):
    """Parameters
    ----------
    expr : sympy.Expr
    x : sympy.Symbol
        Independent variable to plot
    params : dict
        `sympy.Symbol`s to manipulate over.
        syntax is {symbol : (init, start, stop)}
    xdata : numpy.ndarray
        X data to plot
    lambdify_kws : dict, optional
        Keyword arguments to be passed to sympy.lambdify
    plot_kws : dict, optional
        Keyword arguments to be passed to matplotlib.plot
    use_latex : bool, optional
        Default is `False`

    Returns
    -------
    params : dict
        final values of parameters
    """
    if plot_kws is None:
        plot_kws = {}
    if lambdify_kws is None:
        lambdify_kws = {}

    # Create the function we will manipulate
    fcn = sp.lambdify((x, (params.keys())), expr, **lambdify_kws)
    fcn = vectorize(fcn, excluded=[1])
    init_vals = {k: v[0] for k, v in params.items()}

    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()
    line, = ax.plot(xdata, fcn(xdata, init_vals.values()))

    # adjust the main plot to make room for the sliders
    num_vary_params = len(params)
    plt.subplots_adjust(left=0.25, bottom=0.1+0.04*num_vary_params)

    # Make a horizontal slider to control the params.
    param_sliders = {}
    for i, (k, v) in enumerate(params.items()):
        axfreq = plt.axes([0.25, 0.1+i*0.04, 0.65, 0.03])
        if use_latex:
            label = '$'+str(k)+'$'
        else:
            label = str(k)
        param_sliders[k] = Slider(
            ax=axfreq,
            label=label,
            valmin=v[1],
            valmax=v[2],
            valinit=v[0],
        )

    # The function to be called anytime a slider's value changes
    init_min = min(fcn(xdata, init_vals.values()))
    init_max = max(fcn(xdata, init_vals.values()))

    def update(val):
        vals = tuple(param_sliders[k].val for k in params.keys())
        ydata = fcn(xdata, vals)
        old_bottom, old_top = ax.get_ylim()
        line.set_ydata(
            ydata,
        )
        ax.set_ylim(
            bottom=min(old_bottom, min(ydata)),
            top=max(old_top, max(ydata)),
        )
        fig.canvas.draw_idle()

    # register the update function with each slider
    for slider in param_sliders.values():
        slider.on_changed(update)

    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    axresetax = plt.axes([0.6, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')
    button2 = Button(axresetax, 'Reset Axes', hovercolor='0.975')

    def reset(event):
        for slider in param_sliders.values():
            slider.reset()
        ax.set_ylim(bottom=init_min, top=init_max)

    def reset_axes(event):
        vals = tuple(param_sliders[k].val for k in params.keys())
        ydata = fcn(xdata, vals)
        ax.set_ylim(bottom=min(ydata), top=max(ydata))
    button.on_clicked(reset)
    button2.on_clicked(reset_axes)

    plt.show()
    return {k: param_sliders[k].val for k in params.keys()}
