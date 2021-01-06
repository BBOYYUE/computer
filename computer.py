"""
cpu 模拟器
"""

"""
0 COFFEE BREAK 停止
1 ADD 加法
2 SUBTRACT 减法
3 STORE 将数据保存到内存
5 LOAD 读取内存中的数据
6 无条件转移指令
7 为0转移
8 为正转移
901 INPUT 接受输入指令
902 OUTPUT 输出数据
"""

class Computer():
	"""Simulate the CPU """

	def __init__(self):
		"""指令集"""
		self.Instructions = [0,1,2,3,5,6,7,8,901,902]
		"""指令集对应的操作"""
		self.Method = ['M_HEAD','M_ADD','M_SUBTRACT','M_STORE','M_LOAD','M_GOTO','M_EMPTY','M_TRUE','M_INPUT','M_OUTPUT']
		"""需要I/O的操作"""
		self.IoMethod = ['M_INPUT','M_OUTPUT']
		"""会转移指针位置的操作"""
		self.MovePositionMehtod = ['M_GOTO','M_EMPTY','M_TRUE']
		"""会载入载出内存的操作"""
		self.MemoryMethod = ['M_STORE','M_LOAD']
		"""计算器操作"""
		self.ComputerMethod = ['M_ADD','M_SUBTRACT']
		"""会中止脚本的操作"""
		self.StopMethod = ['M_HEAD']
		"""所有的内存地址,一共100位"""
		self.Memory = [value for value in range(0,101)]
		"""指令当前的位置"""
		self.Position = 0
		"""寄存器的值"""
		self.Register = 0
		"""数据缓存"""
		self.cache = []
		"""当前的指令"""
		self.Instruction = 0
		"""当前的数据"""
		self.data = 0
		
	
		
	def coffeeBreak(self):
		self.Position = 0

	"""开始运行"""
	def start(self,start = 1):
		print('程序运行开始:')
		while start:	
			"""从内存中读取数据"""
			if self.readMemory(self.Position):
				"""指令的运行结果决定是否需要继续执行程序"""
				start = self.run()
			else:
				print("发生异常,程序已退出.")
				return
		"""结束之后重置指针"""
		# print(self.cache,self.data,self.Position)
		self.coffeeBreak()
		print('程序运行结束;')

	"""指令的运行"""
	def run(self):
		"""首先验证程序是否正确"""
		if len(self.Instructions) != len(self.Method):
			print('指令集和操作数量不符')
			return False
		"""获取指令"""
		self.getInstruction(self.Position)
		"""获取数据"""
		self.getData(self.Position)
		# print(self.Position,self.data,self.Instruction)
		"""通过指令寻找操作方法"""
		i = 0	
		for val in self.Instructions:
			if val == self.Instruction:
				return self.toMethod(i)
			else:
				i += 1

		"""不存在指令,返回False"""
		if i > len(self.Instructions):
			print('程序出现异常,需要终止')
			return False				

	def toMethod(self,Instruction):
		method = self.Method[Instruction]

		if method in self.IoMethod:
			"""如果需要IO就调取 IO 方法"""
			return self.toIoMethod()
		elif method in self.MovePositionMehtod:
			"""如果需要移动指针就调取移动指针方法"""
			return self.toMovePositionMehtod()
		elif method in self.MemoryMethod:
			"""如果需要操作内存就调取操作内存方法"""
			return self.toMemoryMethod()
		elif method in self.ComputerMethod:
			"""如果需要计算就调用计算方法"""
			return self.toComputerMethod()
		elif method in self.StopMethod:
			"""如果需要中断脚本就调用中断脚本方法"""
			"""只要返回 False ,程序就会中断"""
			return False
		else:
			"""其他情况也返回False"""
			return False

	"""获取指针"""
	def getInstruction(self,Position):
		data = str(self.cache[Position])
		if int(self.cache[Position]) in self.Instructions:
			self.Instruction = int(self.cache[Position])
		elif data != '':
			self.Instruction = int(data[0])
		else:
	 		self.Instruction = 0


	"""获取数据"""
	def getData(self,Position):
		data = str(self.cache[Position])[1:]
		if data != '':
			self.data = int(data)
		else:
			self.data = 0


	"""从内存中读取某一行"""
	def readMemory(self,Position):
		"""获取缓存"""
		get_cache = self.getCache() 

		"""如果没有数据,那么终止程序"""
		if get_cache == False:
			print("数据损坏")
			return False

		"""如果指针已经到最后一行了,那么结束"""
		if Position >= len(self.Memory):
			self.data = 0
		
		return True

	def getCache(self):
		if self.cache == []:
			with open('memory') as meory_content:
				cache = meory_content.readlines()

			if cache == [] or len(cache) > len(self.Memory):
				return False
			
			for item in cache:
				self.cache.append(int(item))

		return True

	def addPosition(self):
		self.Position += 1
		return True

	"""IO方法"""
	def toIoMethod(self):
		if self.Instruction == 901:
			data = input("请输入一个数字:\n\r")
			self.Register = int(data)
		elif self.Instruction == 902:
			print("结果为:")
			print(self.Register)

		return self.addPosition();


	"""指针跳转的方法"""
	def toMovePositionMehtod(self):
		Instruction = self.Instruction
		to_position = self.data
		if Instruction == 6 and to_position < len(self.Memory):
			"""如果是无条件跳转,并且目的地在合理范围内"""
			self.Position = to_position
		elif Instruction == 7 and to_position < len(self.Memory):
			"""如果是为0跳转,并且值为0,并且目的地在合理范围内"""
			if self.Register == 0:
				self.Position = to_position
			else:
				self.Position += 1
		elif Instruction == 8 and to_position < len(self.Memory):
			"""如果是为正跳转,并且值为0,并且目的地在合理范围内"""
			if self.Register > 0:
				self.Position = to_position
			else:
				self.Position += 1
		else:
			print('内存泄露,程序已终止.')
			return False
		return True

	"""内存操作方法"""
	def toMemoryMethod(self):
		Instruction = self.Instruction
		to_position = self.data

		if Instruction == 3:
			"""往指定的行写入的方法"""
			"""首先更新缓存"""
			self.cache[to_position] = self.Register
			"""写入文件"""
			with open('memory','w') as meory_content:
				i = 1
				for item in self.cache:
					if i == len(self.Memory):
						"""最后一行不加换行符"""
						line = str(item)
					else:
						"""后面添加换行符"""
						line = str(item)+"\n" 

					i += 1
					meory_content.write(line)
		elif Instruction == 5:
			"""载入内存中某一行的数据"""
			self.Register = self.cache[to_position]

		return self.addPosition();

	"""计算器方法"""
	def toComputerMethod(self):
		Instruction = self.Instruction
		to_position = self.data

		if to_position < len(self.Memory):
			data = self.cache[to_position]
		else:
			print('内存泄露,程序已终止.')
			return False

		if Instruction == 1:
			self.Register += data
		elif Instruction == 2:
			if self.Register - data > 0:
				self.Register -= data
			else:
				self.Register = 0
		else:
			print('程序出现异常,需要终止')
			return False

		return self.addPosition();

c = Computer()
c.start()