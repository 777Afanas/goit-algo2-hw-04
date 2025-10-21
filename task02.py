class TrieNode:
    """
    Вузол префіксного дерева.
    Використовується в класі Trie.
    """
    def __init__(self):
        # Діти, як звичайний словник
        self.children = {}
        # Значення, що позначає кінець слова
        self.value = None

class Trie:
    """
    Базовий клас префіксного дерева з основними операціями.
    """
    def __init__(self):
        self.root = TrieNode()
        self.size = 0

    def put(self, key, value=None):
        """Вставляє ключ і пов'язане з ним значення."""
        if not isinstance(key, str) or not key:
            raise TypeError(f"Illegal argument for put: key = {key} must be a non-empty string")

        current = self.root
        for char in key:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        if current.value is None:
            self.size += 1
        current.value = value

    def get(self, key):
        """Отримує значення, пов'язане з ключем."""
        if not isinstance(key, str) or not key:
            raise TypeError(f"Illegal argument for get: key = {key} must be a non-empty string")

        current = self.root
        for char in key:
            if char not in current.children:
                return None
            current = current.children[char]
        return current.value

    def delete(self, key):
        """Видаляє ключ із дерева."""
        if not isinstance(key, str) or not key:
            raise TypeError(f"Illegal argument for delete: key = {key} must be a non-empty string")

        def _delete(node, key, depth):
            if depth == len(key):
                if node.value is not None:
                    node.value = None
                    self.size -= 1
                    return len(node.children) == 0
                return False

            char = key[depth]
            if char in node.children:
                should_delete = _delete(node.children[char], key, depth + 1)
                if should_delete:
                    del node.children[char]
                    return len(node.children) == 0 and node.value is None
            return False

        return _delete(self.root, key, 0)

    def is_empty(self):
        """Перевіряє, чи порожнє дерево."""
        return self.size == 0

    def longest_prefix_of(self, s):
        """Повертає найдовший ключ у дереві, що є префіксом заданого рядка s."""
        if not isinstance(s, str) or not s:
            raise TypeError(f"Illegal argument for longestPrefixOf: s = {s} must be a non-empty string")

        current = self.root
        longest_prefix = ""
        current_prefix = ""
        for char in s:
            if char in current.children:
                current = current.children[char]
                current_prefix += char
                if current.value is not None:
                    longest_prefix = current_prefix
            else:
                break
        return longest_prefix

    def keys_with_prefix(self, prefix):
        """Повертає всі ключі у дереві, що починаються з заданого префікса."""
        if not isinstance(prefix, str):
            raise TypeError(f"Illegal argument for keysWithPrefix: prefix = {prefix} must be a string")

        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]

        result = []
        self._collect(current, list(prefix), result)
        return result

    def _collect(self, node, path, result):
        """Допоміжний рекурсивний метод для збору всіх ключів."""
        if node.value is not None:
            result.append("".join(path))
        for char, next_node in node.children.items():
            path.append(char)
            self._collect(next_node, path, result)
            path.pop()

    def keys(self):
        """Повертає всі ключі (слова) у дереві."""
        result = []
        self._collect(self.root, [], result)
        return result

    def _count_words(self, node):
        """Рекурсивно підраховує кількість слів, що закінчуються у піддереві від даного вузла."""
        # Якщо вузол є кінцем слова, додаємо 1 до лічильника
        count = 1 if node.value is not None else 0
        
        # Рекурсивно додаємо кількість слів з усіх дочірніх піддерев
        for child in node.children.values():
            count += self._count_words(child)
        return count

    def count_words_with_prefix(self, prefix):
        """
        Підраховує кількість слів із заданим префіксом. 
        Складність: O(L), де L - довжина префікса.
        """
        if not isinstance(prefix, str):
            raise TypeError(f"Illegal argument for count_words_with_prefix: prefix = {prefix} must be a string")

        current = self.root
        for char in prefix:
            if char not in current.children:
                return 0
            current = current.children[char]
        
        # Викликаємо рекурсивну функцію з вузла, де закінчується префікс
        return self._count_words(current)


# --- Клас Homework з розширеним функціоналом ---

class Homework(Trie):
    """
    Розширений клас Trie з оптимізованими методами для суфіксів та префіксів.
    """

    def __init__(self):
        # Ініціалізуємо основне Trie
        super().__init__()
        # Ініціалізуємо обернене Trie для ефективного пошуку суфіксів
        self.reverse_trie = Trie()

    def put(self, key, value=None):
        """Вставляє ключ в обидва Trie: звичайне та обернене."""
        # 1. Вставляємо в основне Trie
        super().put(key, value)
        
        # 2. Вставляємо обернений ключ в обернене Trie
        self.reverse_trie.put(key[::-1], value)

    # Метод _get_all_words видалено, оскільки він більше не потрібен

    def count_words_with_suffix(self, pattern) -> int:
        """
        Підраховує кількість слів у Trie, що закінчуються на заданий суфікс (pattern).
        Складність: O(P), де P - довжина суфікса, завдяки використанню оберненого Trie.
        """
        if not isinstance(pattern, str):
            raise TypeError(f"Некоректний аргумент: pattern = {pattern} має бути рядком (str).")

        # Реверсуємо патерн. Пошук суфікса "ion" (в основному Trie) 
        # еквівалентний пошуку префікса "noi" (в оберненому Trie).
        reversed_pattern = pattern[::-1]

        # Використовуємо ефективний метод пошуку префіксів на оберненому дереві.
        return self.reverse_trie.count_words_with_prefix(reversed_pattern)

    def has_prefix(self, prefix) -> bool:
        """
        Перевіряє наявність хоча б одного слова із заданим префіксом.
        Складність: O(L), де L - довжина префікса.
        """
        if not isinstance(prefix, str):
            raise TypeError(f"Некоректний аргумент: prefix = {prefix} має бути рядком (str).")

        current = self.root
        for char in prefix:
            # Якщо символу немає в дочірніх елементах, префікс не існує
            if char not in current.children:
                return False
            current = current.children[char]

        # Якщо ми успішно дійшли до кінця префікса, він існує
        return True

if __name__ == "__main__":
    
    trie = Homework()
    words = ["apple", "application", "banana", "cat", "bat", "rate", "complete"]
    # print(f"Вставляємо слова: {words}") # Зауважте: тепер put викликає вставку в два дерева

    for i, word in enumerate(words):
        trie.put(word, i)

    # -------------------------------------------------------------------------
    # Тестування count_words_with_suffix (ОПТИМІЗОВАНИЙ)
    print("\n--- Тестування count_words_with_suffix (O(P)) ---")
    
    # 1. Суфікс "e" (apple, rate, complete)
    pattern_e = "e"
    count_e = trie.count_words_with_suffix(pattern_e)
    print(f"Кількість слів із суфіксом '{pattern_e}': {count_e}")
    assert count_e == 3

    # 2. Суфікс "ion" (application)
    pattern_ion = "ion"
    count_ion = trie.count_words_with_suffix(pattern_ion)
    print(f"Кількість слів із суфіксом '{pattern_ion}': {count_ion}")
    assert count_ion == 1

    # 3. Суфікс "a" (banana)
    pattern_a = "a"
    count_a = trie.count_words_with_suffix(pattern_a)
    print(f"Кількість слів із суфіксом '{pattern_a}': {count_a}")
    assert count_a == 1

    # 4. Суфікс "at" (cat, bat)
    pattern_at = "at"
    count_at = trie.count_words_with_suffix(pattern_at)
    print(f"Кількість слів із суфіксом '{pattern_at}': {count_at}")
    assert count_at == 2

    # 5. Суфікс, якого немає
    pattern_xyz = "xyz"
    count_xyz = trie.count_words_with_suffix(pattern_xyz)
    print(f"Кількість слів із суфіксом '{pattern_xyz}': {count_xyz}")
    assert count_xyz == 0
    
    # -------------------------------------------------------------------------
    # Тестування has_prefix (O(L))
    print("\n--- Тестування has_prefix (O(L)) ---")

    prefix_app = "app"
    has_app = trie.has_prefix(prefix_app)
    print(f"Чи існує префікс '{prefix_app}': {has_app}")
    assert has_app == True

    prefix_batx = "batx"
    has_batx = trie.has_prefix(prefix_batx)
    print(f"Чи існує префікс '{prefix_batx}': {has_batx}")
    assert has_batx == False
    

    # Існуючий префікс "ban" (banana)
    prefix_ban = "ban"
    has_ban = trie.has_prefix(prefix_ban)
    print(f"Чи існує префікс '{prefix_ban}': {has_ban}")
    assert has_ban == True

    # Існуючий префікс "ca" (cat)
    prefix_ca = "ca"
    has_ca = trie.has_prefix(prefix_ca)
    print(f"Чи існує префікс '{prefix_ca}': {has_ca}")
    assert has_ca == True
    
    # Перевірка на слово
    prefix_cat = "cat"
    has_cat = trie.has_prefix(prefix_cat)
    print(f"Чи існує префікс '{prefix_cat}': {has_cat}")
    assert has_cat == True

    # -------------------------------------------------------------------------
    # Тестування обробки помилок
    print("\n--- Тестування обробки помилок ---")

    try:
        trie.has_prefix(123)
    except TypeError as e:
        print(f"Успішно перехоплено помилку для has_prefix: {e}")

    try:
        trie.count_words_with_suffix(["list"])
    except TypeError as e:
        print(f"Успішно перехоплено помилку для count_words_with_suffix: {e}")

    # print("\n--- Усі тести успішно пройдені! ---")





