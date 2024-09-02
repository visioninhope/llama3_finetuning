import torch
from datasets import load_dataset


def processing(sample,
               tokenizer):
    c = sample["chosen"]
    r = sample["rejected"]
    chosen = c[-2:]
    rejected = r[-2:]

    # print("chosen", chosen) # this should be chosen
    # print("rejected", rejected) # this should be rejected
    assert chosen[0] == rejected[0], "prompt not matched"
    prompt = chosen[0]


    history = []
    # print(len(c), len(r))
    for i in range(0, len(c), 2):  # this should be added to prompt
        c_pair = c[i:i+2]
        r_pair = r[i:i+2]
        if c_pair[0] == r_pair[0] and c_pair[1] not in chosen:
            history += c_pair

    history += [prompt]
    return {
        "prompt": tokenizer.apply_chat_template([prompt], tokenize=True,),
        "chosen": tokenizer.apply_chat_template([chosen[1]], tokenize=True),
        "rejected": tokenizer.apply_chat_template([rejected[1]], tokenize=True),
     }

def get_dataset(
    dataset_name: str,
    tokenizer):
    raw_dataset = load_dataset(
        dataset_name,
        trust_remote_code=True,
        revision="main",  # tag name, or branch name, or commit hash
        )

    return {
        dataset: raw_dataset[dataset].map(
            processing,
            batched=False,
            remove_columns=[n for n in raw_dataset.column_names if n not in ["train", "test"]],
            fn_kwargs={"tokenizer": tokenizer,}) for dataset in ["train", "test"]
        }
