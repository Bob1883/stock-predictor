import g4f
from g4f.Provider import (
    Bing,
    Bard,
    Aichat
)


# rate this article: 1 2 3 4 5

response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    provider=g4f.Provider.Aichat,
    messages=[{"role": "system", "content": """Only respond with a number from 1-00 detailing the impact the following article and headline will have on the stock price, 1 being a super negative impact and 100 being a really positive impact:
 Mazda's CEO has said that Tesla is the only company seeing real success in a fragile EV landscape, with other electric cars "not taking off."

Masahiro Moro told Fortune that consumers are still not sold on electric vehicles, with EVs making up just a fraction of the US market and cars piling up in dealerships as demand slows.

"EV is absolutely important technology, and we are developing it. But [in the US] EVs last year [were] about 6% of the market. This year it is 8%. And out of that 8%, 57% was Tesla. Other EVs are not taking off, inventory is piling up," he said.

Tesla continues to dominate the US EV market. While Elon Musk's company has cut prices multiple times in the past year in the face of competition from legacy automakers, it still commands over half the market, with experts estimating that it will take a decade for rivals to catch up.

Unlike automakers like Ford and General Motors, who have unveiled their own EV ranges in an attempt to challenge Tesla, Mazda has been more cautious.

The company has said that it wants at least 25% of its cars to be electric by 2030. It recently killed off its only EV sold in the US, the Mazda MX-30, after reportedly selling just 66 of them this year. It continues to be sold abroad, however.

Moro's comments come at a moment of reckoning for the EV industry. Major auto companies have cut back on targets and spending amid slowing demand, with dealers having to turn away supplies and a lack of cheap EV options hurting adoption.

Ford has postponed a $12 billion investment in electric manufacturing, while General Motors has abandoned plans to build 500,000 EVs by the first half of 2024.

Despite this, sales are on the rise, with more than 1 million electric vehicles expected to be sold in the US this year for the first time, according to Atlas Public Policy.

Moro suggested that a lack of charging stations was one of the major reasons why companies are struggling to hit their target of producing only zero-emission vehicles."""}],
    stream=True,
    
)

for message in response:
    print(message)