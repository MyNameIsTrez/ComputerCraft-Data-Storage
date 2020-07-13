const fruitBasket = {
	apple: 27,
	grape: 0,
	pear: 14
}

const fruitsToGet = ['apple', 'grape', 'pear']

const sleep = ms => {
	return new Promise(resolve => setTimeout(resolve, ms))
}

const getNumFruit = fruit => {
	return sleep(1000).then(v => fruitBasket[fruit])
}

const mapLoop = async _ => {
	console.log('Start')

	const promises = fruitsToGet.map(async fruit => {
		const numFruit = await getNumFruit(fruit)
		return numFruit
	})

	const numFruits = await Promise.all(promises)
	console.log(numFruits)

	console.log('End')
}

mapLoop()