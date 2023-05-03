import re

from zeno import DistillReturn, distill

finder = "Subject:(.*)"


@distill
def subject(df, ops):
    ret_subjs = []
    for entry in df[ops.data_column]:
        ret_subjs.append(re.search(finder, entry[1]["content"]).group(1))

    return DistillReturn(distill_output=ret_subjs)
