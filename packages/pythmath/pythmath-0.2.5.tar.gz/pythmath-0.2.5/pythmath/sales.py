from pythmath.math import percentage, percent


def discount(val, per_off, tax=False, tax_perc=None):
    """
    Calculates the discounted price based on percentage.

    :param val: Value.
    :param per_off: percent off value.
    :param tax: flag to include tax in discount.
    :param tax_perc: tax percentage.
    :return: Discounted price either with or without tax.
    """
    perc_off = percent(per_off)
    disc = val * percentage(per_off, 100) / 100
    disc_price = val - (val * perc_off)
    if tax:
        tax_per = tax_perc
        tax_amount = disc_price * percent(tax_per)
        tax_price = tax_amount + disc_price
        saved = val * percent(tax_per) / per_off + disc
        return tax_price, saved
    else:
        return disc, disc_price


def gst_amount(val, tax_per):
    """
    Helps you find out either net or gross price of
    your product based on a percentage-based GST
    (Goods and Services Tax) rate.

    :param val: Value.
    :param tax_per: percent off value.
    :return: Discounted price.
    """
    tax_off = percent(tax_per)
    return val + (val * tax_off)


def gross_sales(price, products_sold):
    """
    Calculates the gross sales.

    :param price: Price.
    :param products_sold: Number of products sold.
    :return: Gross Sales from price and products sold.
    """
    return products_sold * price


def net_sales(gross_sales, sales_returns=0, allowances=0, sales_discount=0):
    """
    Calculates the net sales.

    :param gross_sales: Price.
    :param sales_returns: Value of sales return.
    :param allowances: Value of allowances.
    :param sales_discount: Value of sales discount.
    :return: Gross Sales from price and products sold.
    """
    return gross_sales - (sales_returns + allowances + sales_discount)


def sales_tax(val, tax_perc):
    """
    Calculates the sales tax.

    :param val: Value or price.
    :param tax_perc: Tax Percentage (int value such as 20 or 50).
    :return: Sales Tax.
    """
    tax_per = percent(tax_perc)
    tax_amount = val * tax_per
    tax_price = val + tax_amount
    return tax_amount, tax_price


def vat(net_price, vat_perc):
    """
    Calculates the value added tax.

    :param net_price: Value of net price.
    :param vat_perc: Value added tax percentage (int value such as 20 or 50).
    :return: Value added sales tax.
    """
    vat_per = percent(vat_perc)
    vat_amount = net_price * vat_per
    vat_price = net_price + vat_amount
    return vat_amount, vat_price


def revenue(cost, markup_perc):
    """
    Calculates the revenue from given cost and markup percentage.

    :param cost: Value of cost.
    :param markup_perc: Markup Percentage (int 25 or 50).
    :return: Total sales revenue.
    """
    markup_per = percent(markup_perc)
    return cost + cost * markup_per


def profit(revenue, cost):
    """
    Calculates the profit.

    :param revenue: Revenue value.
    :param cost: Value of cost.
    :return: Total profit.
    """
    return revenue - cost


def markup(cost, profit):
    """
    Calculates the markup percentage.

    :param cost: Value of cost.
    :param profit: profit value.
    :return: Markup percentage.
    """
    return 100 * profit / cost


def commission(price, comm_perc):
    """
    Calculates the commission.

    :param price: Value of price.
    :param comm_perc: Commission Percentage (int value such as 20 or 50).
    :return: Commission from price and percentage.
    """
    comm_per = percent(comm_perc)
    return price * comm_per


def margin(revenue, cost):
    """
    Calculates the margin from revenue and cost.

    :param revenue: Value of revenue.
    :param cost: Value of cost.
    :return: Margin from revenue and cost.
    """
    return 100 * (revenue - cost) / revenue
