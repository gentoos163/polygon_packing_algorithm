import copy
import random
from tools import nfp_utls


class GeneticAlgorithm():
    """
    Генетические алгоритмы
    """

    def __init__(self, adam, bin_polygon, config):
        """
        Инициализируйте параметры и сгенерируйте группы генов в соответствии с параметрами
        :param adam: графика
        :param bin_polygon: 面布
        :param config: Параметры алгоритма
        """
        self.bin_bounds = bin_polygon['points']
        self.bin_bounds = {
            'width': bin_polygon['width'],
            'height': bin_polygon['height'],
        }
        self.config = config
        self.bin_polygon = bin_polygon
        angles = list()  # 添加角度
        shapes = copy.deepcopy(adam)
        for shape in shapes:
            angles.append(self.random_angle(shape))

        # 基因群，图形顺序和图形旋转的角度作为基因编码
        self.population = [{'placement': shapes, 'rotation': angles}]

        for i in range(1, self.config['populationSize']):
            mutant = self.mutate(self.population[0])
            self.population.append(mutant)

    def random_angle(self, shape):
        """
        随机旋转角度的选取
        :param shape:
        :return:
        """
        angle_list = list()
        for i in range(0, self.config['rotations']):
            angle_list.append(i * (360 / self.config['rotations']))

        # 打乱顺序
        def shuffle_array(data):
            for i in range(len(data) - 1, 0, -1):
                j = random.randint(0, i)
                data[i], data[j] = data[j], data[i]
            return data

        angle_list = shuffle_array(angle_list)

        # 查看选择后图形是否能放置在里面
        for angle in angle_list:
            rotate_part = nfp_utls.rotate_polygon(shape[1]['points'], angle)
            # 是否判断旋转出界,没有出界可以返回旋转角度,rotate 只是尝试去转，没有真正改变图形坐标
            if rotate_part['width'] < self.bin_bounds['width'] and rotate_part['height'] < self.bin_bounds['height']:
                return angle  # 将angle_list[i] 修改为angle

        return 0

    def mutate(self, individual):  # 变异1：交换两个物品的排放位置   变异2：转换一个物品的角度
        clone = {
            'placement': individual['placement'][:],
            'rotation': individual['rotation'][:]
        }
        for i in range(0, len(clone['placement'])):
            if random.random() < 0.01 * self.config['mutationRate']:
                if i + 1 < len(clone['placement']):
                    clone['placement'][i], clone['placement'][i + 1] = clone['placement'][i + 1], clone['placement'][i]

        if random.random() < 0.01 * self.config['mutationRate']:
            clone['rotation'][i] = self.random_angle(clone['placement'][i])
        return clone

    def generation(self):
        # 适应度 从大到小排序
        self.population = sorted(self.population, key=lambda a: a['fitness'])
        new_population = [self.population[0]]
        while len(new_population) < self.config['populationSize']:
            male = self.random_weighted_individual()
            female = self.random_weighted_individual(male)
            # 交集下一代
            children = self.mate(male, female)

            # 轻微突变
            new_population.append(self.mutate(children[0]))

            if len(new_population) < self.config['populationSize']:
                new_population.append(self.mutate(children[1]))

        print('new :', new_population)
        self.population = new_population

    def random_weighted_individual(self, exclude=None):
        pop = self.population
        if exclude and pop.index(exclude) >= 0:
            pop.remove(exclude)

        rand = random.random()
        lower = 0
        weight = 1.0 / len(pop)
        upper = weight
        pop_len = len(pop)
        for i in range(0, pop_len):
            if (rand > lower) and (rand < upper):
                return pop[i]
            lower = upper
            upper += 2 * weight * float(pop_len - i) / pop_len
        return pop[0]

    def mate(self, male, female):
        cutpoint = random.randint(0, len(male['placement']) - 1)
        gene1 = male['placement'][:cutpoint]
        rot1 = male['rotation'][:cutpoint]

        gene2 = female['placement'][:cutpoint]
        rot2 = female['rotation'][:cutpoint]

        def contains(gene, shape_id):
            for i in range(0, len(gene)):
                if gene[i][0] == shape_id:
                    return True
            return False

        for i in range(len(female['placement']) - 1, -1, -1):
            if not contains(gene1, female['placement'][i][0]):
                gene1.append(female['placement'][i])
                rot1.append(female['rotation'][i])

        for i in range(len(male['placement']) - 1, -1, -1):
            if not contains(gene2, male['placement'][i][0]):
                gene2.append(male['placement'][i])
                rot2.append(male['rotation'][i])

        return [{'placement': gene1, 'rotation': rot1}, {'placement': gene2, 'rotation': rot2}]