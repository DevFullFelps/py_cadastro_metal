from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import plotly.express as px

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metalurgica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class MateriaPrima(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String(50), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    fornecedor = db.Column(db.String(50), nullable=False)
    data_entrada = db.Column(db.String(10), nullable=False)
    corrida = db.Column(db.String(50), nullable=False)



@app.route('/')
def home():
    todos_os_materiais = MateriaPrima.query.all()
    
    return render_template('cadastro.html', materiais=todos_os_materiais)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    material = request.form.get('material')
    peso = float(request.form.get('peso'))
    fornecedor = request.form.get('fornecedor')
    data = request.form.get('data')
    corrida = request.form.get('corrida')
    
    materiais_validos = ['Aço Carbono', 'Alumínio', 'Latão', 'Inox']
    fornecedores_validos = ['Alumass', 'Metalnox', 'SNK', 'Latumi']
    if material not in materiais_validos:
        return "ERRO: O material enviado não é válido!", 400
    if fornecedor not in fornecedores_validos:
        return "ERRO: O fornecedor enviado não é válido!", 400
    
    novo_item = MateriaPrima(
        material = material,
        peso = peso,
        fornecedor = fornecedor,
        data_entrada = data,
        corrida = corrida
    )
    
    db.session.add(novo_item)
    db.session.commit()
    
    return redirect(url_for('home'))

@app.route('/buscar_registro/<int:id>')
def buscar_registro(id):
    registro = MateriaPrima.query.get(id)
    if not registro:
        return jsonify({'erro': 'Registro não encontrado'}), 404
    
    return jsonify({
        'material': registro.material,
        'peso': registro.peso,
        'fornecedor': registro.fornecedor,
        'data': registro.data_entrada,
        'corrida': registro.corrida
    })


@app.route('/deletar', methods=['Post'])
def deletar():
    id_registro = request.form.get('id_registro')
    chave_gerente = request.form.get('chave_gerente')
    
    CHAVE_CORRETA = 'gerente123'
    
    if chave_gerente != CHAVE_CORRETA:
        return "ERRO: Chave de acesso do gerente incorreta!", 403
    
    registro = MateriaPrima.query.get(id_registro)

    if not registro:
        return "ERRO: Registro não encontrado!", 404
    
    db.session.delete(registro)
    db.session.commit()
    
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    materiais = MateriaPrima.query.all()
    
    dados = [{
        'material': m.material,
        'peso': m.peso,
        'fornecedor': m.fornecedor,
        'data': m.data_entrada
    } for m in materiais]
    df = pd.DataFrame(dados)
    df['material'] = df['material'].astype('category')
    df['fornecedor'] = df['fornecedor'].astype('category')
    df['data'] = pd.to_datetime(df['data'], format="%Y-%m-%d")
    
    df_by_data = df.groupby('data')['peso'].sum().reset_index()
    
    fig = px.bar(
        df,
        x='material',
        y='peso',
        color='fornecedor',
        title='Total de Peso (Kg) por Tipo de Material'
    )
    
    fig_pizza = px.pie(
        df,
        values='peso',
        names='fornecedor',
        title='Participação dos Fornecedores por Peso Total'
    )
    
    fig_linha = px.line(
        df_by_data,
        x='data',
        y='peso',
        title='Evolução Diária de Entrada de Matéria-Prima (Kg)'
        )
    
    grafico_barras = fig.to_html(full_html=False)
    grafico_pizza = fig_pizza.to_html(full_html=False)
    grafico_linha = fig_linha.to_html(full_html=False)
    return render_template(
        'dashboard.html',
        grafico_barras=grafico_barras,
        grafico_pizza=grafico_pizza,
        grafico_linha=grafico_linha
        )

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)