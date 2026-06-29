import math


class Pagination:

    def __init__(self, items, page=1, per_page=9):

        self.total = len(items)

        self.page = page

        self.per_page = per_page

        self.pages = max(
            1,
            math.ceil(self.total / self.per_page)
        )

        start = (page - 1) * per_page
        end = start + per_page

        self.items = items[start:end]

    @property
    def has_prev(self):

        return self.page > 1

    @property
    def has_next(self):

        return self.page < self.pages

    @property
    def prev_num(self):

        if self.has_prev:
            return self.page - 1

        return None

    @property
    def next_num(self):

        if self.has_next:
            return self.page + 1

        return None

    def iter_pages(
        self,
        left_edge=2,
        left_current=2,
        right_current=2,
        right_edge=2
    ):

        last = 0

        for num in range(
            1,
            self.pages + 1
        ):

            if (
                num <= left_edge
                or (
                    self.page - left_current
                    <= num
                    <= self.page + right_current
                )
                or num > self.pages - right_edge
            ):

                if last + 1 != num:

                    yield None

                yield num

                last = num