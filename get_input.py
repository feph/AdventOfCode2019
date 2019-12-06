import requests

AOC_SESSION = open("aoc_session.txt").read().strip()

def get_aoc_input(day):
    input_url = f'https://adventofcode.com/2019/day/{day}/input'
    cookies = {'session': AOC_SESSION}
    r = requests.get(input_url, cookies=cookies)
    if not r.ok:
        raise ValueError(r.text)
    return [l for l in r.iter_lines()]

if __name__ == "__main__":
    i = get_aoc_input(1)
    print(i)
