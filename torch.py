import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import time

print("🔥 SIFIRDON KERAS - TAM ÇALIŞAN SİSTEM")
print("=" * 50)


class Activations:
    """Aktivasyon fonksiyonları ve türevleri"""
    
    @staticmethod
    def sigmoid(x):
        """Sigmoid: 0-1 arası çıktı, binary classification için"""
        x = np.clip(x, -500, 500)  # Numerik stabilite
        return 1 / (1 + np.exp(-x))
    
    @staticmethod
    def sigmoid_derivative(x):
        """Sigmoid türevi: geri yayılım için"""
        return x * (1 - x)
    
    @staticmethod
    def relu(x):
        """ReLU: Negatifleri sıfırlar, hidden layer'lar için"""
        return np.maximum(0, x)
    
    @staticmethod
    def relu_derivative(x):
        """ReLU türevi: pozitifler için 1, negatifler için 0"""
        return (x > 0).astype(float)
    
    @staticmethod
    def tanh(x):
        """Tanh: -1 ile 1 arası, RNN'ler için iyi"""
        return np.tanh(x)
    
    @staticmethod
    def tanh_derivative(x):
        """Tanh türevi"""
        return 1 - x ** 2
    
    @staticmethod
    def softmax(x):
        """Softmax: Çoklu sınıflandırma için, çıktıları olasılığa çevirir"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))  # Numerik stabilite
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    @staticmethod
    def linear(x):
        """Linear: Regression için, girdiyi olduğu gibi döndürür"""
        return x
    
    @staticmethod
    def linear_derivative(x):
        """Linear türevi: her zaman 1"""
        return np.ones_like(x)
    
    @staticmethod
    def get_activation(name):
        """İsme göre aktivasyon fonksiyonu ve türevini getir"""
        activations = {
            'sigmoid': (Activations.sigmoid, Activations.sigmoid_derivative),
            'relu': (Activations.relu, Activations.relu_derivative),
            'tanh': (Activations.tanh, Activations.tanh_derivative),
            'softmax': (Activations.softmax, None),  # Özel durum
            'linear': (Activations.linear, Activations.linear_derivative)
        }
        return activations.get(name, (None, None))
    


class Losses:
    """Loss fonksiyonları ve türevleri"""
    
    @staticmethod
    def mse(y_true, y_pred):
        """
        Mean Squared Error - Regression için
        Ortalama Kare Hata: mean((y_true - y_pred)^2)
        """
        return np.mean((y_true - y_pred) ** 2)
    
    @staticmethod
    def mse_derivative(y_true, y_pred):
        """MSE türevi: 2 * (y_pred - y_true) / n"""
        return 2 * (y_pred - y_true) / y_true.size
    
    @staticmethod
    def binary_crossentropy(y_true, y_pred):
        """
        Binary Cross Entropy - İkili sınıflandırma için
        -mean(y_true * log(y_pred) + (1-y_true) * log(1-y_pred))
        """
        y_pred = np.clip(y_pred, 1e-12, 1 - 1e-12)  # Numerik stabilite
        return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    
    @staticmethod
    def binary_crossentropy_derivative(y_true, y_pred):
        """Binary Cross Entropy türevi"""
        y_pred = np.clip(y_pred, 1e-12, 1 - 1e-12)
        return (y_pred - y_true) / (y_pred * (1 - y_pred)) / y_true.size
    
    @staticmethod
    def categorical_crossentropy(y_true, y_pred):
        """
        Categorical Cross Entropy - Çoklu sınıflandırma için  
        -mean(sum(y_true * log(y_pred), axis=1))
        """
        y_pred = np.clip(y_pred, 1e-12, 1 - 1e-12)
        return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))
    
    @staticmethod
    def categorical_crossentropy_derivative(y_true, y_pred):
        """Categorical Cross Entropy türevi (softmax ile basit)"""
        return (y_pred - y_true) / y_true.shape[0]
    
    @staticmethod
    def get_loss(name):
        """İsme göre loss fonksiyonu ve türevini getir"""
        losses = {
            'mse': (Losses.mse, Losses.mse_derivative),
            'binary_crossentropy': (Losses.binary_crossentropy, Losses.binary_crossentropy_derivative),
            'categorical_crossentropy': (Losses.categorical_crossentropy, Losses.categorical_crossentropy_derivative)
        }
        return losses.get(name)
class SGD:
    """
    Stochastic Gradient Descent - En basit optimizer
    FORMÜL: w = w - learning_rate * gradient
    """
    
    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate
    
    def update(self, params, grads):
        """Parametreleri güncelle: w = w - lr * gradient"""
        for key in params.keys():
            params[key] -= self.learning_rate * grads[key]

class MomentumSGD:
    """
    Momentum SGD - Geçmiş gradient'leri hatırlar
    FORMÜL: 
        velocity = momentum * velocity - lr * gradient  
        w = w + velocity
    """
    
    def __init__(self, learning_rate=0.01, momentum=0.9):
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.velocity = None
    
    def initialize_velocity(self, params):
        """Hız vektörünü sıfırla"""
        self.velocity = {}
        for key, value in params.items():
            self.velocity[key] = np.zeros_like(value)
    
    def update(self, params, grads):
        if self.velocity is None:
            self.initialize_velocity(params)
        
        for key in params.keys():
            # Hızı güncelle
            self.velocity[key] = self.momentum * self.velocity[key] - self.learning_rate * grads[key]
            # Ağırlığı güncelle
            params[key] += self.velocity[key]

class Adam:
    """
    Adam - Adaptive Moment Estimation (En popüler optimizer)
    Momentum + Adaptive learning rate birleşimi
    """
    
    def __init__(self, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = None  # Birinci moment (momentum)
        self.v = None  # İkinci moment (scale)
        self.t = 0     # Adım sayısı
    
    def initialize_moments(self, params):
        """Momentları sıfırla"""
        self.m = {}
        self.v = {}
        for key, value in params.items():
            self.m[key] = np.zeros_like(value)
            self.v[key] = np.zeros_like(value)
    
    def update(self, params, grads):
        if self.m is None:
            self.initialize_moments(params)
        
        self.t += 1
        
        for key in params.keys():
            # Momentları güncelle
            self.m[key] = self.beta1 * self.m[key] + (1 - self.beta1) * grads[key]
            self.v[key] = self.beta2 * self.v[key] + (1 - self.beta2) * (grads[key] ** 2)
            
            # Bias düzeltmesi
            m_hat = self.m[key] / (1 - self.beta1 ** self.t)
            v_hat = self.v[key] / (1 - self.beta2 ** self.t)
            
            # Ağırlığı güncelle
            params[key] -= self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)

class Optimizers:
    """Optimizer fabrikası"""
    
    @staticmethod
    def get_optimizer(name, learning_rate=0.01, **kwargs):
        if name == 'sgd':
            return SGD(learning_rate=learning_rate)
        elif name == 'momentum':
            return MomentumSGD(learning_rate=learning_rate, **kwargs)
        elif name == 'adam':
            return Adam(learning_rate=learning_rate, **kwargs)
        else:
            raise ValueError(f"Bilinmeyen optimizer: {name}")
class Metrics:
    """Model değerlendirme metrikleri"""
    
    @staticmethod
    def accuracy(y_true, y_pred):
        """Classification accuracy"""
        if y_true.shape[1] > 1:  # Multi-class
            true_labels = np.argmax(y_true, axis=1)
            pred_labels = np.argmax(y_pred, axis=1)
        else:  # Binary
            true_labels = (y_true > 0.5).astype(int).flatten()
            pred_labels = (y_pred > 0.5).astype(int).flatten()
        return np.mean(true_labels == pred_labels)
    
    @staticmethod
    def binary_accuracy(y_true, y_pred):
        """Binary classification accuracy"""
        y_pred_binary = (y_pred > 0.5).astype(int)
        return np.mean(y_true == y_pred_binary)
    
    @staticmethod
    def categorical_accuracy(y_true, y_pred):
        """Categorical accuracy"""
        true_labels = np.argmax(y_true, axis=1)
        pred_labels = np.argmax(y_pred, axis=1)
        return np.mean(true_labels == pred_labels)
    
    @staticmethod
    def mae(y_true, y_pred):
        """Mean Absolute Error - Regression için"""
        return np.mean(np.abs(y_true - y_pred))
    
    @staticmethod
    def get_metric(name):
        """İsme göre metriği getir"""
        metrics = {
            'accuracy': Metrics.accuracy,
            'binary_accuracy': Metrics.binary_accuracy,
            'categorical_accuracy': Metrics.categorical_accuracy,
            'mae': Metrics.mae
        }
        return metrics.get(name)
class Dense:
    """
    Dense (Fully Connected) Layer
    Yapı: Girdi → Ağırlık Çarpımı → Bias Ekleme → Aktivasyon
    """
    
    def __init__(self, units, input_dim=None, activation='relu', 
                 kernel_initializer='he_normal'):
        """
        Args:
            units: Nöron sayısı
            input_dim: Girdi boyutu (ilk katmanda zorunlu)
            activation: Aktivasyon fonksiyonu
            kernel_initializer: Ağırlık ilkleme yöntemi
        """
        self.units = units
        self.input_dim = input_dim
        self.activation_name = activation
        self.activation, self.activation_derivative = Activations.get_activation(activation)
        self.kernel_initializer = kernel_initializer
        
        # Parametreler
        self.weights = None
        self.bias = None
        
        # Cache'ler (geri yayılım için)
        self.input = None
        self.output = None
        self.z = None  # Aktivasyon öncesi
        
        # Eğer input_dim verildiyse hemen initialize et
        if input_dim is not None:
            self._initialize_parameters()
    
    def _initialize_parameters(self):
        """Ağırlık ve bias'ları initialize et"""
        # Ağırlık ilkleme
        if self.kernel_initializer == 'he_normal':
            # ReLU için optimal: sqrt(2.0 / fan_in)
            scale = np.sqrt(2.0 / self.input_dim)
            self.weights = np.random.randn(self.input_dim, self.units) * scale
        elif self.kernel_initializer == 'xavier_normal':
            # Sigmoid/Tanh için: sqrt(1.0 / fan_in)
            scale = np.sqrt(1.0 / self.input_dim)
            self.weights = np.random.randn(self.input_dim, self.units) * scale
        else:  # random_normal
            self.weights = np.random.randn(self.input_dim, self.units) * 0.01
        
        # Bias ilkleme (genelde sıfır)
        self.bias = np.zeros((1, self.units))
    
    def build(self, input_shape):
        """Input shape'i alıp parametreleri initialize et"""
        if self.weights is None:
            self.input_dim = input_shape[-1]
            self._initialize_parameters()
    
    def forward(self, inputs):
        """
        İLERİ YAYILIM:
        1. Lineer dönüşüm: z = inputs * weights + bias
        2. Aktivasyon: output = activation(z)
        """
        self.input = inputs
        
        # Lineer dönüşüm
        self.z = np.dot(inputs, self.weights) + self.bias
        
        # Aktivasyon
        if self.activation:
            self.output = self.activation(self.z)
        else:
            self.output = self.z
            
        return self.output
    
    def backward(self, doutput, optimizer):
        """
        GERİ YAYILIM:
        1. Aktivasyon türevi
        2. Gradyan hesaplama (dw, db)
        3. Optimizer ile güncelleme
        4. Önceki katmana gradient iletme
        """
        batch_size = self.input.shape[0]
        
        # Aktivasyon türevi (zincir kuralı)
        if self.activation_derivative and self.activation_name != 'softmax':
            dactivation = self.activation_derivative(self.output)
            dz = doutput * dactivation
        else:
            dz = doutput
        
        # Gradyanları hesapla
        dw = np.dot(self.input.T, dz) / batch_size
        db = np.sum(dz, axis=0, keepdims=True) / batch_size
        dinput = np.dot(dz, self.weights.T)
        
        # OPTIMIZER İLE GÜNCELLE
        params = {'weights': self.weights, 'bias': self.bias}
        grads = {'weights': dw, 'bias': db}
        optimizer.update(params, grads)
        
        # Güncellenmiş parametreleri kaydet
        self.weights = params['weights']
        self.bias = params['bias']
        
        return dinput  # Önceki katmana iletilmek üzere
    
    def get_parameters(self):
        """Parametreleri getir (kaydetme/yükleme için)"""
        return {'weights': self.weights, 'bias': self.bias}
    
    def set_parameters(self, params):
        """Parametreleri set et (kaydetme/yükleme için)"""
        self.weights = params['weights']
        self.bias = params['bias']
class Sequential:
    """
    Sequential Model - Katmanları sıralı çalıştırır
    Keras'taki Sequential model'in aynısı
    """
    
    def __init__(self):
        self.layers = []
        self.built = False
        self.history = {
            'loss': [],
            'val_loss': [],
            'accuracy': [],
            'val_accuracy': []
        }
        
        # Compile parametreleri
        self.optimizer = None
        self.loss_function = None
        self.loss_derivative = None
        self.metrics = None
        self.metric_names = None
    
    def add(self, layer):
        """Modele katman ekle"""
        self.layers.append(layer)
        self.built = False
    
    def compile(self, optimizer='sgd', loss='mse', metrics=None):
        """
        Modeli derle - Keras'taki gibi
        Args:
            optimizer: 'sgd', 'momentum', 'adam'
            loss: 'mse', 'binary_crossentropy', 'categorical_crossentropy'  
            metrics: ['accuracy', 'mae'] gibi
        """
        print("🔄 Model derleniyor...")
        
        # Optimizer seç
        if isinstance(optimizer, str):
            self.optimizer = Optimizers.get_optimizer(optimizer)
        else:
            self.optimizer = optimizer
        
        # Loss fonksiyonu seç
        loss_funcs = Losses.get_loss(loss)
        if loss_funcs:
            self.loss_function, self.loss_derivative = loss_funcs
        else:
            raise ValueError(f"Bilinmeyen loss function: {loss}")
        
        # Metrikleri ayarla
        self.metrics = []
        self.metric_names = []
        if metrics:
            for metric in metrics:
                metric_func = Metrics.get_metric(metric)
                if metric_func:
                    self.metrics.append(metric_func)
                    self.metric_names.append(metric)
        
        self.built = True
        print("✅ Model başarıyla derlendi!")
    
    def build(self, input_shape):
        """Modeli build et - tüm katmanları initialize et"""
        print("🔨 Model build ediliyor...")
        current_shape = input_shape
        for i, layer in enumerate(self.layers):
            layer.build(current_shape)
            if hasattr(layer, 'units'):
                current_shape = (current_shape[0], layer.units)
            print(f"  Katman {i+1}: {current_shape}")
        self.built = True
    
    def forward(self, X, training=True):
        """Tüm katmanlarda ileri yayılım"""
        output = X
        for layer in self.layers:
            output = layer.forward(output)
        return output
    
    def backward(self, X, y, y_pred):
        """Tüm katmanlarda geri yayılım"""
        # Loss gradient'i hesapla
        dloss = self.loss_derivative(y, y_pred)
        
        # Katmanlarda geriye doğru ilerle
        doutput = dloss
        for layer in reversed(self.layers):
            doutput = layer.backward(doutput, self.optimizer)
        
        return doutput
    
    def compute_metrics(self, y_true, y_pred, prefix=''):
        """Tüm metrikleri hesapla"""
        metric_results = {}
        for metric_name, metric_func in zip(self.metric_names, self.metrics):
            metric_value = metric_func(y_true, y_pred)
            metric_results[f'{prefix}{metric_name}'] = metric_value
        return metric_results
    
    def fit(self, X, y, epochs=100, batch_size=32, validation_split=0.0, 
            validation_data=None, shuffle=True, verbose=1):
        """
        Modeli eğit - Keras'taki gibi
        Args:
            X: Eğitim verisi
            y: Hedef verisi  
            epochs: Epoch sayısı
            batch_size: Batch boyutu
            validation_split: Validation için ayırma oranı
            validation_data: Direkt validation data
            shuffle: Veriyi karıştır
            verbose: Log seviyesi
        """
        
        # Model build edilmemişse build et
        if not self.built:
            self.build(X.shape)
        
        # Validation data hazırla
        X_train, y_train = X, y
        X_val, y_val = None, None
        
        if validation_data is not None:
            X_val, y_val = validation_data
        elif validation_split > 0:
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=validation_split, shuffle=shuffle, random_state=42
            )
        
        # Eğitim parametreleri
        n_samples = X_train.shape[0]
        n_batches = int(np.ceil(n_samples / batch_size))
        
        print(f"🚀 Eğitim başlıyor...")
        print(f"   Örnek sayısı: {n_samples}")
        print(f"   Batch size: {batch_size}") 
        print(f"   Batch sayısı: {n_batches}")
        print(f"   Epochs: {epochs}")
        if X_val is not None:
            print(f"   Validation örnekleri: {X_val.shape[0]}")
        print("-" * 50)
        
        # EĞİTİM DÖNGÜSÜ
        for epoch in range(epochs):
            epoch_start = time.time()
            
            # Veriyi karıştır
            if shuffle:
                indices = np.random.permutation(n_samples)
                X_shuffled = X_train[indices]
                y_shuffled = y_train[indices]
            else:
                X_shuffled = X_train
                y_shuffled = y_train
            
            epoch_loss = 0
            batch_metrics = {name: 0 for name in self.metric_names}
            
            # BATCH DÖNGÜSÜ
            for batch_idx in range(n_batches):
                # Batch'i al
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, n_samples)
                X_batch = X_shuffled[start_idx:end_idx]
                y_batch = y_shuffled[start_idx:end_idx]
                
                # 1. İLERİ YAYILIM
                y_pred = self.forward(X_batch)
                
                # 2. LOSS HESAPLA
                batch_loss = self.loss_function(y_batch, y_pred)
                epoch_loss += batch_loss
                
                # 3. METRİKLERİ HESAPLA
                batch_metric_results = self.compute_metrics(y_batch, y_pred)
                for name, value in batch_metric_results.items():
                    batch_metrics[name] += value
                
                # 4. GERİ YAYILIM
                self.backward(X_batch, y_batch, y_pred)
            
            # EPOCH SONU - ORTALAMALARI HESAPLA
            epoch_loss /= n_batches
            epoch_metrics = {name: value / n_batches for name, value in batch_metrics.items()}
            
            # VALIDATION HESAPLA
            val_loss = None
            val_metrics = {}
            
            if X_val is not None:
                y_val_pred = self.forward(X_val, training=False)
                val_loss = self.loss_function(y_val, y_val_pred)
                val_metrics = self.compute_metrics(y_val, y_val_pred, 'val_')
            
            # HISTORY'E KAYDET
            self.history['loss'].append(epoch_loss)
            if val_loss is not None:
                self.history['val_loss'].append(val_loss)
            
            for metric_name in self.metric_names:
                self.history[metric_name].append(epoch_metrics.get(metric_name, 0))
                if f'val_{metric_name}' in val_metrics:
                    self.history[f'val_{metric_name}'].append(val_metrics[f'val_{metric_name}'])
            
            # LOG YAZDIR
            epoch_time = time.time() - epoch_start
            
            if verbose == 1 and epoch % max(1, epochs // 10) == 0:
                log_message = f"Epoch {epoch+1}/{epochs} - {epoch_time:.2f}s - loss: {epoch_loss:.4f}"
                
                for metric_name in self.metric_names:
                    metric_value = epoch_metrics.get(metric_name, 0)
                    log_message += f" - {metric_name}: {metric_value:.4f}"
                
                if val_loss is not None:
                    log_message += f" - val_loss: {val_loss:.4f}"
                    for metric_name in self.metric_names:
                        val_metric_value = val_metrics.get(f'val_{metric_name}', 0)
                        log_message += f" - val_{metric_name}: {val_metric_value:.4f}"
                
                print(log_message)
        
        print("✅ Eğitim tamamlandı!")
        return self.history
    
    def predict(self, X):
        """Tahmin yap"""
        return self.forward(X, training=False)
    
    def evaluate(self, X, y, verbose=1):
        """Modeli değerlendir"""
        y_pred = self.predict(X)
        loss = self.loss_function(y, y_pred)
        metrics = self.compute_metrics(y, y_pred)
        
        if verbose:
            print(f"📊 Değerlendirme Sonuçları:")
            print(f"   Loss: {loss:.4f}")
            for name, value in metrics.items():
                print(f"   {name}: {value:.4f}")
        
        return [loss] + list(metrics.values())
    
    def summary(self):
        """Model özetini yazdır"""
        print("\n📋 Model Özeti:")
        print("=" * 60)
        total_params = 0
        
        for i, layer in enumerate(self.layers):
            if hasattr(layer, 'weights') and layer.weights is not None:
                layer_params = layer.weights.size + layer.bias.size
                total_params += layer_params
                
                print(f"Katman {i+1}: Dense")
                print(f"  Girdi: {layer.input_dim if hasattr(layer, 'input_dim') else '?'}")
                print(f"  Çıktı: {layer.units}")
                print(f"  Aktivasyon: {layer.activation_name}")
                print(f"  Parametre: {layer_params:,}")
                print("-" * 40)
        
        print(f"Toplam parametre: {total_params:,}")
        print(f"Eğitilebilir parametre: {total_params:,}")
        print("=" * 60)
    
    def plot_history(self):
        """Eğitim geçmişini görselleştir"""
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # Loss grafiği
        axes[0].plot(self.history['loss'], label='Eğitim Loss', linewidth=2)
        if 'val_loss' in self.history and self.history['val_loss']:
            axes[0].plot(self.history['val_loss'], label='Validation Loss', linewidth=2)
        axes[0].set_title('Model Loss')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Loss')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Metrics grafiği
        if self.metric_names:
            for metric_name in self.metric_names:
                if metric_name in self.history:
                    axes[1].plot(self.history[metric_name], label=f'Eğitim {metric_name}', linewidth=2)
                if f'val_{metric_name}' in self.history:
                    axes[1].plot(self.history[f'val_{metric_name}'], label=f'Validation {metric_name}', linewidth=2)
            axes[1].set_title('Model Metrics')
            axes[1].set_xlabel('Epoch')
            axes[1].set_ylabel('Metric Değeri')
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()













# HIZLI KULLANIM ÖRNEKLERİ
def quick_examples():
    """Hızlı kullanım örnekleri"""
    
    print("\n⚡ HIZLI KULLANIM ÖRNEKLERİ")
    print("=" * 50)
    
    # ÖRNEK 1: Basit Regression
    print("\n1. Basit Regression Modeli:")
    X_simple = np.random.randn(100, 3)
    y_simple = 2 * X_simple[:, 0:1] + 3 * X_simple[:, 1:2] - 1 * X_simple[:, 2:3] + 0.1 * np.random.randn(100, 1)
    
    model1 = Sequential()
    model1.add(Dense(10, input_dim=3, activation='relu'))
    model1.add(Dense(1, activation='linear'))
    
    model1.compile(optimizer='sgd', loss='mse')
    model1.fit(X_simple, y_simple, epochs=50, batch_size=16, verbose=0)
    
    test_pred = model1.predict(X_simple[:5])
    print(f"Gerçek: {y_simple[:5].flatten()}")
    print(f"Tahmin: {test_pred.flatten()}")
    
    # ÖRNEK 2: Basit Binary Classification
    print("\n2. Basit Binary Classification:")
    X_bin_simple = np.random.randn(100, 2)
    y_bin_simple = (X_bin_simple[:, 0] + X_bin_simple[:, 1] > 0).astype(int).reshape(-1, 1)
    
    model2 = Sequential()
    model2.add(Dense(5, input_dim=2, activation='relu'))
    model2.add(Dense(1, activation='sigmoid'))
    
    model2.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model2.fit(X_bin_simple, y_bin_simple, epochs=50, batch_size=16, verbose=0)
    
    accuracy = model2.evaluate(X_bin_simple, y_bin_simple, verbose=0)[1]
    print(f"Model Doğruluğu: {accuracy:.4f}")

# Hızlı örnekleri çalıştır
quick_examples()
    

    