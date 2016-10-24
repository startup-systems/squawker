class SquawksController < ApplicationController
  def index
    @squawks = Squawk.order(created_at: :desc)
  end

  def show
    @squawk = Squawk.find(params[:id])
  end

  def new
  end

  def create
    squawk = Squawk.new(squawk_params)
    if squawk.save
      redirect_to "/squawks/#{squawk.id}"
    else
      redirect_to "/squawks/new"
    end
  end

  def edit
    @squawk = Squawk.find(params[:id])
  end

  def update
    squawk = Squawk.find(params[:id])
    if squawk.update(squawk_params)
      redirect_to "/squawks/#{squawk.id}"
    else
      redirect_to "/squawks/#{squawk.id}/edit"
    end
  end

  def destroy
    squawk = Squawk.find(params[:id])
    squawk.destroy
    redirect_to "/squawks"
  end

  private
  def squawk_params
    params.require(:squawk).permit(:author, :content, :image_url)
  end
end
