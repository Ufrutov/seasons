# Seasons

#### Manual data collect script

It should be launched at the page web console

```
const videoEl = document.getElementById('htmlPlayer').getElementsByTagName('video')[0];
const listEl = Array.from(document.getElementById('htmlPlayer_playlist').children);
let output = [];

listEl.forEach((el, i) => {
	setTimeout(() => {
		if( i !== 0 )
			el.click();

		setTimeout(() => {
			console.info(`[${i+1}:${listEl.length}] src: ${videoEl['src']}`);
			output.push({
				id: 's1',
				name: 'Царь горы',
				season: 1,
				epizode: i+1,
				src: videoEl['src']
			});

			if( i === listEl.length-1 )
				console.log(JSON.stringify(output));
		}, 1500);
	}, i*2000);
});
```

#### Python Selenium data collect

```
$ python selenium.py
```

Python script collects all available episodes and store them at the `data.js` file