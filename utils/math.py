class Math:
    @staticmethod
    def clamp(value: float, min_value: float, max_value: float) -> float:
        """
        Returns a value clamped between a min and max

        Parameters
        ----------
        value : float
            The original value to be clamped
        min_value : float
            The minimum value (lower limit)
        max_value : float
            The maximum value (upper limit)

        Returns
        -------
        float
            The clamped value
        """
        return max(min(value, max_value), min_value)

    @staticmethod
    def clamp_01(value: float) -> float:
        """
        Returns a value clamped between 0 and 1

        Parameters
        ----------
        value : float
            The original value to be clamped

        Returns
        -------
        float
            The clamped value
        """
        return Math.clamp(value, 0.0, 1.0)

    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        """
        Linearly interpolates between the points a and b by the interpolant t. The parameter t is clamped to the range [0, 1].

        Use Case
        --------
        When t = 0, returns a
        When t = 1, returns b
        When t = 0.5, returns the midpoint of a and b

        Parameters
        ----------
        a : float
            The start value, returned when t = 0
        b : float
            The start value, returned when t = 1
        t : float
            The value used to interpolate between a and b

        Returns
        -------
        float
            The interpolated float result between the two float values
        """
        t = Math.clamp_01(t)
        return a + (b - a) * t