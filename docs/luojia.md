# Luojia

## Radiance Calculation

From the website:

> The absolute radiance is floating-point data, which is inconvenient to store. Therefore, the floating-point data is amplified by $10^{10}$ times and then stretched exponentially to the integer, and the standard storage format of the LuoJia1-01 images is INT32. Users can convert the INT32 standard images to the radiance according to the radiance conversion formula provided by the data download website.
>
> The radiance conversion formula of LuoJia1-01 image data is an exponential equation, as follows
> $$
> L = DN^{3/2} \cdot 10^{-10}
> $$
> where $L$ is the input radiance ($W/(m^2 \cdot sr\mu m)$), $DN$ is the digital number of LuoJia1-01 images.

