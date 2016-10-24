class CreateSquawks < ActiveRecord::Migration
  def change
    create_table :squawks do |t|
      t.string :author
      t.text :content
      t.string :image_url
      t.timestamps
    end
  end
end
