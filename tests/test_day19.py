from solutions.day19 import Filter, FilterSet


def test_calculate_possibilities() -> None:
    filters = [
        "px{a<2006:qkq,m>2090:A,rfg}",
        "pv{a>1716:R,A}",
        "lnx{m>1548:A,A}",
        "rfg{s<537:gd,x>2440:R,A}",
        "qs{s>3448:A,lnx}",
        "qkq{x<1416:A,crn}",
        "crn{x>2662:A,R}",
        "in{s<1351:px,qqz}",
        "qqz{s>2770:qs,m<1801:hdj,R}",
        "gd{a>3333:R,R}",
        "hdj{m>838:A,pv}",
    ]
    filter_set = FilterSet(Filter.from_line(line) for line in filters)
    print("\n")
    assert filter_set.calculate_possibilities() == 167409079868000
